"""配置文件 - Configurations"""

import os
import shutil
import toml

def load_toml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = toml.load(file)
    return config

def save_toml_config(file_path, config):
    with open(file_path, 'w', encoding='utf-8') as file:
        toml.dump(config, file)

def get_config_value(config, section, key):
    try:
        # 支持嵌套的键
        keys = section.split('.') + [key]
        value = config
        for k in keys:
            value = value[k]
        return value
    except KeyError:
        return None

def ensure_resource_existence(resource_directory, target_relative_path, source_packaged_path):  
    # 确保资源文件夹存在  
    expanded_resource_directory = os.path.expanduser(resource_directory)  
    if not os.path.exists(expanded_resource_directory):  
        os.makedirs(expanded_resource_directory)  
    
    # 构造目标路径  
    target_path = os.path.join(expanded_resource_directory, target_relative_path)  
    
    # 检查目标路径是否存在  
    if not os.path.exists(target_path):  
        # 判断是文件还是文件夹  
        if os.path.isfile(source_packaged_path):  
            # 复制文件  
            shutil.copy2(source_packaged_path, target_path)  
        elif os.path.isdir(source_packaged_path):  
            # 复制文件夹  
            shutil.copytree(source_packaged_path, target_path)  
        else:  
            # 原始路径既不是文件也不是文件夹，抛出异常或处理错误  
            raise FileNotFoundError(f"The source packaged resource '{source_packaged_path}' does not exist.")  

def overwrite_resource(resource_directory, target_relative_path, source_packaged_path):  
    # 确保资源文件夹存在  
    expanded_resource_directory = os.path.expanduser(resource_directory)  
    if not os.path.exists(expanded_resource_directory):  
        os.makedirs(expanded_resource_directory)  
    
    # 构造目标路径  
    target_path = os.path.join(expanded_resource_directory, target_relative_path)  
    
    # 判断是文件还是文件夹  
    if os.path.isfile(source_packaged_path):  
        # 如果是文件，直接覆盖  
        shutil.copy2(source_packaged_path, target_path)  
    elif os.path.isdir(source_packaged_path):  
        # 如果是文件夹，先尝试删除目标文件夹（如果存在），然后复制  
        if os.path.exists(target_path):  
            shutil.rmtree(target_path)  # 强制删除目标文件夹及其内容  
        shutil.copytree(source_packaged_path, target_path)  
    else:  
        # 原始路径既不是文件也不是文件夹，抛出异常或处理错误  
        raise FileNotFoundError(f"The source packaged resource '{source_packaged_path}' does not exist.")  
  

# 默认从环境变量读取数据文件夹的位置 不存在则回退到默认的位置~/.config/LaphaeLaicmd
resource_dir = os.getenv('laphaelaicmd_linux_config_dir', os.path.join('~', '.config', 'LaphaeLaicmd'))
resource_dir = os.path.expanduser(resource_dir)

# path to ensure in resource_dir
resource_required_ensure = ["data/","locales"]
for resource_required_ensure_dir in resource_required_ensure:  
    ensure_resource_existence(resource_dir,resource_required_ensure_dir, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), resource_dir))

ai_settings_path = os.path.join(resource_dir, "data", "AI_settings.toml")
config_path = os.path.join(resource_dir, "data", "config.toml")
cli_outputs_path = os.path.join(resource_dir, "data", "_cli_outputs.toml")

ai_settings = load_toml_config(ai_settings_path)
config = load_toml_config(config_path)

ai_name = get_config_value(ai_settings, "info", "select_ai")
if ai_name is not None:
    ai_model = get_config_value(ai_settings, f"info.{ai_name}", "model")
    My_key = get_config_value(ai_settings, f"info.{ai_name}", "api_key")
else:
    ai_model = None
    My_key = None

instruction_prompt = get_config_value(ai_settings, "prompt", "text")
custom_instruct = get_config_value(ai_settings, "custom_instruct", "text")


# 打印的发言人名称颜色
program_name_color = get_config_value(config, "display", "program_name_color")
user_name_color = get_config_value(config, "display", "user_name_color")
system_name_color = get_config_value(config, "display", "system_name_color")
ai_name_color = get_config_value(config, "display", "ai_name_color")

# AI输出文本打印的颜色
ai_print_color = get_config_value(config, "display", "ai_print_color")


# 定义初始名称
program_name = "AIcmd"
user_name = "User"
system_name = "System"
system_version = "System version unkown"

if __name__ == "__main__":
    print("AI Name:", ai_name)
    print("API Key:", My_key)
    print("Model:", ai_model)
    print("color:", ai_name_color)
