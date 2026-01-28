import json


class botMixin:
    """
    Bot Mixin
    """
    
    def startBot(self,file_name):
        """
        startBot
        """
        print("start Bot")

        # Get File with json using utf-8
        import os

        # Get File with json using utf-8
        with open(file_name, encoding="utf8") as json_file:
            data = json.load(json_file)
            
        # Resolve relative paths relative to the config file location
        config_dir = os.path.dirname(os.path.abspath(file_name))
        
        if "project" in data:
            # Resolve project file path
            if "project_file" in data["project"]:
                proj_path = data["project"]["project_file"]
                if not os.path.isabs(proj_path):
                    data["project"]["project_file"] = os.path.abspath(os.path.join(config_dir, proj_path))
                    print(f"Resolved project path: {data['project']['project_file']}")
            
            # Resolve output directory
            if "output_dir" in data["project"]:
                out_dir = data["project"]["output_dir"]
                if not os.path.isabs(out_dir):
                    data["project"]["output_dir"] = os.path.abspath(os.path.join(config_dir, out_dir))
                    print(f"Resolved output dir: {data['project']['output_dir']}")

        self.startAfterEffect(data)
