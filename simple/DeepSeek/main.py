import zipfile, json, os, re

ZIP_FILE = './deepseek_data-2026-05-05.zip'
OUTPUT_DIR = './deepseek_chats'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def node_Selector(mapping: dict):
    """
    从 Deepseek 的 mapping 树结构中提取最终采用的对话路径
    处理逻辑：
    1.从根节点（parent=None）开始
    2.遇到多个子节点（重新生成），选create_time最新的
    3.跳过 message 为 None 的节点
    """

    messages = []

    for node_id, node in mapping.items():
        msg = node.get('message', {})
        if msg is None: 
            # 跳过无消息的节点
            continue 

        for frag in msg.get('fragments', []):
            content = frag.get('content', '')
            if not content:
                continue # 跳过无内容的fragment

            # role = '用户' if frag_type == 'REQUEST' else '助手'
            # role = 'user' if frag_type == 'REQUEST' else 'assistant'
            frag_type = frag.get('type', '')
            if frag_type == 'REQUEST':  # 当是用户请求时，添加到消息列表
                role = 'user'
                messages.append({
                    'role': role,
                    'content': f"[{role}]: {content}",
                    'parent_id': node.get('parent'),
                    'inserted_at': msg.get('inserted_at', ''),
                    'model': msg.get('model', ''),
                }) # 如果只需要 user 消息，assistant 可以不添加

    # 去重：每个parent_id只保留最新消息
    unique = {}
    for msg in messages:
        parent_id = msg['parent_id']
        # 如果当前消息比已保存的更新，就替换
        if parent_id not in unique or msg['inserted_at'] > unique[parent_id]['inserted_at']:
            unique[parent_id] = msg # 令当前消息为最新消息

    # 吐槽：成了，，，看来我基础有太多遗漏的部分了，，，我都不知道字典可以这样用。。。。
        
    # 按时间排序返回
    result = sorted(unique.values(), key=lambda x: x['inserted_at'])

    # 调试：打印去重后的 parent_id 列表
    # print([f"{m['parent_id']}({m['inserted_at'][-14:]})" for m in result])
    
    return result


data = []

# Step 1: 读取ZIP文件中的JSON文件
with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    for filename in zf.namelist():
        if filename.endswith('.json'):
            data = json.load(zf.open(filename))

            conversations = data if isinstance(data, list) else [data]
            
            # Step 2: 遍历每个对话，提取用户消息
            for conv in conversations:
                title = conv.get('title', 'untitled')
                safe_title = re.sub(r'[<>:"/\\|?*\[\]\{\}\n\r\t]', '', title)[:20] # 限制长度

                mapping = conv.get('mapping', {})

                selected_messages = node_Selector(mapping)

                # Step 4: 保存消息到文件
                if selected_messages:
                    with open(f"{OUTPUT_DIR}/{conv.get('inserted_at', '')[:10]}_{safe_title}.txt", 'w', encoding='utf-8') as f:
                        f.write(f"标题: {title}\n")
                        f.write(f"ID: {conv.get('id', '')}\n")
                        f.write(f"创建时间: {conv.get('inserted_at', '')}\n")
                        f.write(f"更新时间: {conv.get('updated_at', '')}\n")
                        f.write(f"模型: {selected_messages[0].get('model', '')}\n")
                        f.write("="*60 + "\n\n")

                        f.write("\n\n".join([msg['content'] for msg in selected_messages]))
                        
                    print(f"✓ {title}")
                
                # i = 68
                # while i > 0:
                #     i -= 1
                #     break