import subprocess
from func_utils import open_system_browser, set_system_brightness, set_system_volume
import ollama

OLLAMA_MODEL = "qwen3:1.7b"

class FunctionAgent:
    tools=[]
    name_to_func_map={}
    config={"custom_commands":[]}
    def __init__(self,config):
        self.config=config
        print(config)
        custom_tools = self.extract_config_tools()
        self.tools = [
            {
                'type': 'function',
                'function': {
                    'name': 'set_volume',
                    'description': (
                        "Adjusts system audio volume (0-100). Use this for requests about sound, "
                        "noise levels, or muting. Examples: 'make it louder', 'quiet down', 'make it quieter', "
                        "'mute the sound' (level=0), 'increase volume' (level=100)."
                    ),
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'level': {'type': 'integer', 'minimum': 0, 'maximum': 100}
                        },
                        'required': ['level'],
                    },
                },
            },
            {
                'type': 'function',
                'function': {
                    'name': 'set_brightness',
                    'description': (
                        "Adjusts screen backlight intensity (0-100). Use this for requests about "
                        "visibility, eye strain, or power saving. Examples: 'it's too dark' (level=100), "
                        "'dim the screen for a movie', 'half brightness' (level=50)."
                    ),
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'level': {'type': 'integer', 'minimum': 0, 'maximum': 100}
                        },
                        'required': ['level'],
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'open_website',
                    'description': "Open the mentioned website/url, if none is mentioned open the default page. Examples are 'open youtube.com', 'open chat.com' etc.",
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'url': {
                                'type': 'string',
                                'description': "The URL to open. (e.g., https://google.com, https://youtube.com, https://mail.google.com)."
                            }
                        },
                        'required': ['url'],
                    },
                },
            }
        ]
        self.tools.extend(custom_tools)
    def extract_config_tools(self):
        custom_tools=[]
        name_map={}
        for commandObj in self.config["custom_commands"]:
            name=commandObj["name"]
            custom_tools.append({
                    'type': 'function',
                    'function': {
                    'name': name,
                    'description': commandObj["description"],
                },
            })
            name_map[name]=commandObj["command"]
        self.name_to_func_map=name_map
        return custom_tools
            
        
        
    def execute(self, user_command):
        print(f"\n💬 Command: '{user_command}'")

        response = ollama.chat(
            model=OLLAMA_MODEL, 
            messages=[{'role': 'user', 'content': user_command}], 
            tools=self.tools,
            options={'temperature':0},
        )
        
        print("RES",response)

        if response['message'].get('tool_calls'):
            for tool in response['message']['tool_calls']:
                func_name = tool['function']['name']
                args = tool['function']['arguments']
                
                if func_name == 'set_volume':
                    target_level = args.get('level')
                    print(f"🔊 Setting volume to {target_level}%")
                    print(f"   {set_system_volume(target_level)}")
                
                elif func_name == 'set_brightness':
                    target_level = args.get('level')
                    print(f"💡 Setting brightness to {target_level}%")
                    print(f"   {set_system_brightness(target_level)}")
                
                elif func_name == 'open_website':
                    target_url = args.get("url", "https://google.com")
                    print(f"🌐 Opening browser to: {target_url}")
                    print(f"   {open_system_browser(target_url)}")
                else:
                    if func_name in self.name_to_func_map:
                        # Ig, will have to take a look at this later. Not the most secure way to do this.
                        subprocess.run(self.name_to_func_map[func_name],shell=True)
                    
        else:
            print(f"💭 AI Response: {response['message']['content']}")
