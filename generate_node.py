import json
from datetime import datetime, timezone
import uuid

def generate_node_data(id, label, x, y, editor_name, width=300, height=100, creator_editor_id_suffix="LLM", node_type="M"):
    # print(f"width, height {width},{height}")

    # 現在のUTC時刻を取得し、指定された形式に変換
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # ユニークなIDを生成（タイムスタンプ + ランダムな文字列）
    # node_id = f"#{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"

    # creatorとeditorの共通IDを設定
    creator_editor_id_suffix = creator_editor_id_suffix or uuid.uuid4().hex[:10]
    creator_editor_id = f"graphCollab:{creator_editor_id_suffix}"

    # 新しいノードデータを生成
    node_data = {
        "data": {
            "lastModified": current_time,
            "editor": creator_editor_id,
            "creatorName": editor_name,
            "creator": creator_editor_id,
            "label": label,
            "editorName": editor_name,
            "begin": current_time,
            "nodeType": node_type
        },
        "position": {
            "y": float(y),
            "x": float(x)
        },
        "type": "graphNode",
        "width": float(width),
        "positionAbsolute": {
            "x": float(x),
            "y": float(y)
        },
        "dragging": False,
        "id": id,
        "height": float(height)
    }

    return node_data

# 使用例
if __name__ == "__main__":
    # 新しいノードデータを生成
    new_node = generate_node_data(
        id="node1",
        label="新しいノード",
        x=250.0,
        y=250.0,
        editor_name="268",
        width=120.0,
        height=50.0,
        creator_editor_id_suffix="LLM",
        node_type="C"
    )

    # 生成されたノードデータを表示
    print(json.dumps(new_node, indent=2, ensure_ascii=False))
    
    # 生成されたデータからidを取り出す
    node_id = new_node["id"]
    print(f"\n取り出されたノードID: {node_id}")
