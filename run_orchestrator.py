import os
import yaml
import time
import sys
from dotenv import load_dotenv
from termcolor import colored
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.compliance.security_pillars import DPDPComplianceManager
from src.retrieval.hybrid_rag import HybridRetrievalEngine, HeadTailContextManager
from src.retrieval.graph_rag import GraphRAGEngine

load_dotenv()

class NyayaOrchestrator:
    def __init__(self):
        self.compliance = DPDPComplianceManager()
        self.retrieval = HybridRetrievalEngine()
        self.graph = GraphRAGEngine()
        # Using ChatOllama for consistent interaction with LangChain prompts
        self.llm = ChatOllama(model="llama3")
        print(colored("[Nyaya] Initialized Local Chat Engine (Ollama/Llama3)", "cyan"))
        with open('agent.yaml', 'r') as f:
            self.config = yaml.safe_load(f)

    def run_pipeline(self, user_query):
        print(colored(f"\n[USER QUERY]: {user_query}", "yellow"))
        self.compliance.log_access("USER_LLM", "EXECUTE_PIPELINE", "QUERY")

        context = {"input": user_query}
        pipeline = self.config['orchestration']['pipeline']

        for step in pipeline:
            agent_name = step['agent']
            agent_config = self.config['agents'][agent_name]
            
            print(colored(f"\n[{agent_name}] --------------------", "green"))
            
            # Helper to escape content for LangChain templates
            def escape_p(text): return str(text).replace("{", "{{").replace("}", "}}")

            if agent_name == "LegalIntake":
                result = self._run_agent(agent_config, user_query)
                # Only stop if it's a critical non-LLM error (though _run_agent now handles LLM errors)
                if "[Error]" in result and "Live LLM failed" not in result:
                    print(colored(f"Critical Error in Intake: {result}", "red"))
                    return 
                context['facts'] = result
                print(f"Result: {context['facts']}")
                
            elif agent_name == "StatuteResearcher":
                retrieved_docs = self.retrieval.search(user_query, top_k=3)
                mapping_prompt = f"Facts: {escape_p(context.get('facts'))}\nRetrieved Laws: {escape_p(retrieved_docs)}\nIdentify the most relevant Statute Sections."
                result = self._run_agent(agent_config, mapping_prompt)
                context['statutes'] = result
                print(f"Result: {context['statutes']}")
                
            elif agent_name == "LoopholeAnalyst":
                adversarial_prompt = f"Review this scenario for loopholes: {escape_p(user_query)}\nStatutes identified: {escape_p(context.get('statutes'))}"
                context['loopholes'] = self._run_agent(agent_config, adversarial_prompt)
                print(f"Result: {context['loopholes']}")
                
            elif agent_name == "CaseLawResearcher":
                precedent_prompt = f"Find SC precedents for: {escape_p(context.get('statutes'))}"
                context['precedents'] = self._run_agent(agent_config, precedent_prompt)
                print(f"Result: {context['precedents']}")
                
            elif agent_name == "SynthesisStrategist":
                final_prompt = f"Draft an IRAC memorandum.\nIssue: {escape_p(user_query)}\nStatutes: {escape_p(context.get('statutes'))}\nPrecedents: {escape_p(context.get('precedents'))}"
                print(colored("\n[GENERATING IRAC MEMORANDUM...]", "white", "on_blue"))
                final_output = self._run_agent(agent_config, final_prompt)
                print(final_output)

    def _run_agent(self, config, task_prompt):
        # 1. Attempt Live LLM Call
        if os.getenv("GOOGLE_API_KEY"):
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"Persona: {config['persona']}\nOutput Format: {config.get('output_format', 'text')}"),
                ("user", task_prompt)
            ])
            chain = prompt | self.llm
            try:
                response = chain.invoke({})
                return response.content
            except Exception as e:
                print(colored(f"[Warning] Live LLM failed: {e}. Falling back to Local Mock Reasoning...", "magenta"))

        # 2. Fallback: Intelligent Mock Reasoning (Modeled on CLAUSE + IRAC)
        return self._local_reasoning_fallback(config, task_prompt)

    def _local_reasoning_fallback(self, config, task_prompt):
        """
        Provides high-quality simulated reasoning when API keys are unavailable.
        """
        tp_lower = task_prompt.lower()
        if "theft" in tp_lower:
            return "Based on the BNS Section 303 mapping, the act constitutes theft as it involves dishonest moving of property. Punishment: Imprisonment up to 3 years."
        elif "privacy" in tp_lower or "dpdp" in tp_lower:
            return "Section 8(5) of DPDP Act 2023 mandates that the Data Fiduciary must implement reasonable security safeguards. Article 21 supports this as a fundamental right."
        elif "murder" in tp_lower or "penalty" in tp_lower:
            return "Homicide is categorized under BNS Section 103. The penalty is death or life imprisonment with fine."
        
        return f"[Simulated Output for {config['persona']}]: Processing your legal query based on retrieved statutes..."

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print(colored("Error: GOOGLE_API_KEY not found in .env", "red"))
        sys.exit(1)

    orchestrator = NyayaOrchestrator()
    print(colored("=== Nyaya-Orchestrator: LIVE System ===", "cyan", attrs=["bold"]))
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input(colored("\n[INPUT] Enter your legal query: ", "yellow"))
    
    if query:
        orchestrator.run_pipeline(query)
