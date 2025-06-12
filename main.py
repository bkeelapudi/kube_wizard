#!/usr/bin/env python3
"""
Kubernetes Troubleshooting Slack Bot using Strands Agents SDK
"""
import os
import sys
import logging
import re
from dotenv import load_dotenv
from strands import Agent, tool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define the system prompt for the Kubernetes expert
KUBERNETES_EXPERT_SYSTEM_PROMPT = """
You are a Kubernetes troubleshooting expert. Provide clear, detailed explanations and solutions for any Kubernetes issue.
Include practical troubleshooting steps, commands to run, and resolution strategies. If the question is unclear or not 
related to Kubernetes, politely ask for clarification while staying in your role as a Kubernetes expert.

Always format code examples and commands properly using markdown. When appropriate, explain the underlying concepts
to help users understand why the solution works.

Example topics you can help with:
- Pod and container issues (CrashLoopBackOff, ImagePullBackOff, etc.)
- Networking problems (Services, Ingress, DNS resolution)
- Storage issues (PersistentVolumes, StorageClasses)
- RBAC and security configuration
- Resource constraints and scaling
- Cluster management and upgrades
- Helm chart troubleshooting
- Kubernetes API server issues
- etcd database problems
- Control plane component failures
- Node problems and kubelet issues
- Custom Resource Definition (CRD) issues
- Operator troubleshooting
"""

# Define a function to detect Kubernetes questions
def is_kubernetes_question(text):
    """
    Detect if a message contains a Kubernetes question or issue
    """
    # Check for common Kubernetes question indicators
    k8s_patterns = [
        r'kubernetes', r'k8s', r'kubectl', r'pod', r'deployment', r'service',
        r'namespace', r'ingress', r'cluster', r'node', r'container',
        r'configmap', r'secret', r'volume', r'pv', r'pvc', r'storageclass',
        r'daemonset', r'statefulset', r'job', r'cronjob', r'replicaset',
        r'crashloopbackoff', r'imagepullbackoff', r'evicted', r'pending',
        r'rbac', r'serviceaccount', r'role', r'clusterrole', r'helm',
        r'taint', r'toleration', r'affinity', r'cordon', r'drain',
        r'kube-system', r'kube-dns', r'coredns', r'kubelet', r'kubeadm',
        r'minikube', r'kind', r'eks', r'aks', r'gke', r'openshift',
        r'istio', r'knative', r'kustomize', r'operator', r'crd'
    ]
    
    for pattern in k8s_patterns:
        if re.search(r'\b' + pattern + r'\b', text, re.IGNORECASE):
            return True
    
    return False

@tool
def kubernetes_expert(query: str) -> str:
    """
    Process and respond to Kubernetes troubleshooting queries using a specialized Kubernetes agent.
    
    Args:
        query: A Kubernetes question or issue from the user
        
    Returns:
        A detailed Kubernetes troubleshooting answer with explanations and resolution steps
    """
    # Format the query for the Kubernetes agent with clear instructions
    formatted_query = f"Please help troubleshoot the following Kubernetes issue, providing detailed explanations, commands to run, and resolution steps: {query}"
    
    try:
        logger.info("Processing Kubernetes troubleshooting question")
        # Create the Kubernetes agent
        k8s_agent = Agent(
            system_prompt=KUBERNETES_EXPERT_SYSTEM_PROMPT,
        )
        agent_response = k8s_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return "I apologize, but I couldn't process this Kubernetes question. Please check if your query is clearly stated or try rephrasing it with more details about the issue you're experiencing."
    except Exception as e:
        # Return specific error message for Kubernetes query processing
        logger.error(f"Error processing Kubernetes query: {e}", exc_info=True)
        return f"Error processing your Kubernetes troubleshooting query: {str(e)}"

def setup_slack_bot():
    """
    Set up and run the Slack bot
    """
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        
        # Initialize the Slack Bolt app
        app = App(
            token=os.environ.get("SLACK_BOT_TOKEN"),
            signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
        )
        
        # Create the Kubernetes agent
        k8s_agent = Agent(
            system_prompt=KUBERNETES_EXPERT_SYSTEM_PROMPT,
        )
        
        @app.event("message")
        def handle_message_events(event, say):
            """Handle message events in channels"""
            # Skip messages from bots
            if event.get("bot_id"):
                return
                
            # Get the message text
            message_text = event.get("text", "")
            
            # Check if it's a Kubernetes question
            if is_kubernetes_question(message_text):
                # Send a "thinking" message
                thinking_message = say(
                    text=":thinking_face: Analyzing Kubernetes issue...",
                    thread_ts=event.get("ts")
                )
                
                try:
                    # Process the Kubernetes question
                    formatted_query = f"Please help troubleshoot the following Kubernetes issue, providing detailed explanations, commands to run, and resolution steps: {message_text}"
                    response = k8s_agent(formatted_query)
                    
                    # Send the response in a thread
                    say(
                        text=str(response),
                        thread_ts=event.get("ts")
                    )
                except Exception as e:
                    # Send error message
                    say(
                        text=f"I'm sorry, I encountered an error while processing this Kubernetes troubleshooting request: {str(e)}",
                        thread_ts=event.get("ts")
                    )
        
        @app.event("app_mention")
        def handle_app_mention_events(event, say):
            """Handle app mention events"""
            # Get the message text (remove the app mention)
            message_text = event.get("text", "")
            # Remove the app mention part
            message_text = re.sub(r'<@[A-Z0-9]+>', '', message_text).strip()
            
            if not message_text:
                say(
                    text="Hello! I'm a Kubernetes troubleshooting expert. Describe any Kubernetes issue you're facing, and I'll provide detailed resolution steps and commands to help you fix it.",
                    thread_ts=event.get("ts")
                )
                return
                
            # Always process app mentions as potential Kubernetes questions
            try:
                # Send a "thinking" message
                say(
                    text=":thinking_face: Analyzing Kubernetes issue...",
                    thread_ts=event.get("ts")
                )
                
                # Process the Kubernetes question
                formatted_query = f"Please help troubleshoot the following Kubernetes issue, providing detailed explanations, commands to run, and resolution steps: {message_text}"
                response = k8s_agent(formatted_query)
                
                # Send the response in a thread
                say(
                    text=str(response),
                    thread_ts=event.get("ts")
                )
            except Exception as e:
                # Send error message
                say(
                    text=f"I'm sorry, I encountered an error while processing this Kubernetes troubleshooting request: {str(e)}",
                    thread_ts=event.get("ts")
                )
        
        # Start the app
        logger.info("Starting Kubernetes Troubleshooting Slack Bot...")
        handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
        handler.start()
        
    except Exception as e:
        logger.error(f"Failed to initialize Slack bot: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    setup_slack_bot()
