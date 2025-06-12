# Kubernetes Troubleshooting Slack Bot

A simple Slack bot that provides expert Kubernetes troubleshooting assistance for your team using the **Strands Agents SDK**. This bot automatically detects Kubernetes-related questions in channels and provides detailed explanations, troubleshooting steps, and resolution commands.

![kube_wiz](https://github.com/user-attachments/assets/73316058-5208-421b-85b7-cc10465165d1)

## Features

- Automatically detects Kubernetes questions in Slack channels
- Provides detailed troubleshooting steps and commands
- Explains underlying concepts to help with understanding
- Responds in threads to keep channels clean
- Supports a wide range of Kubernetes topics:
  - Pod and container issues
  - Networking problems
  - Storage issues
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

## How It Works

1. Post any Kubernetes question or issue in a Slack channel where the bot is present
2. The bot automatically detects Kubernetes questions and responds with detailed troubleshooting guidance
3. Get comprehensive explanations, commands to run, and resolution steps

## Example Questions

- "My pod is stuck in CrashLoopBackOff state, how do I fix it?"
- "Why can't my service connect to pods with the selector I specified?"
- "How do I debug an ImagePullBackOff error?"
- "My PersistentVolumeClaim is stuck in pending state"
- "What's the best way to troubleshoot RBAC permission issues?"
- "My node is showing NotReady status, how can I diagnose the problem?"

## Installation

1. Clone this repository
2. Run the installation script:
   ```bash
   ./install.sh
   ```
   This will:
   - Create a Python virtual environment
   - Install required dependencies
   - Create a `.env` file from the template

3. Edit the `.env` file with your Slack and AWS credentials

4. Start the bot:
   ```bash
   source venv/bin/activate
   python src/main.py
   ```

## Slack App Setup

1. Create a new Slack app at https://api.slack.com/apps
2. Add the following Bot Token Scopes:
   - `app_mentions:read`
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `reactions:write`
3. Enable Socket Mode
4. Install the app to your workspace
5. Copy the Bot Token, Signing Secret, and App Token to your `.env` file

## Development

For development, you may want to install additional tools:
```bash
pip install pytest black flake8
```

## Configuration

The bot is configured in the `src/main.py` file. You can modify:

- The system prompt for the Kubernetes expert
- Kubernetes question detection patterns
- Response formatting
- Slack event handling

## Technologies Used

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- Amazon Bedrock Claude for AI capabilities (default)
- Slack Bolt SDK for Slack integration
- Python 3.10+

## License

MIT
