import asyncio
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse, unquote
import y_py as Y
from websockets import connect
from ypy_websocket import WebsocketProvider

from generate_node import generate_node_data
from generate_edge import generate_edge_data

def extract_room_id(url: str) -> str:
    """
    URLからRoom IDを抽出する

    Args:
        url (str): 完全なURL (e.g., 'http://localhost:3000/YjsBasedSimpleGraphCollab/graph/fInSyb2JwIE1')

    Returns:
        str: 抽出されたRoom ID

    Raises:
        ValueError: URLの形式が不正な場合
    """
    try:
        # URLをパースしてパスを取得
        path = urlparse(url).path
        # パスの最後の部分をRoom IDとして取得
        room_id = path.split('/')[-1]
        if not room_id:
            raise ValueError("Room ID not found in URL")
        return room_id
    except Exception as e:
        raise ValueError(f"Invalid URL format: {str(e)}")

def parse_arguments() -> argparse.Namespace:
    """
    コマンドライン引数をパースする

    Returns:
        argparse.Namespace: パースされた引数オブジェクト
    """
    parser = argparse.ArgumentParser(
        description='WebSocketを使用してノードとエッジを表示するプログラム',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  python display_node.py analysis_result_0001.json http://localhost:3000/YjsBasedSimpleGraphCollab/graph/fInSyb2JwIE1

注意:
  URLは以下の形式である必要があります: http://hostname/YjsBasedSimpleGraphCollab/graph/roomId
'''
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='ノードとエッジのデータを含む入力JSONファイルのパス'
    )
    parser.add_argument(
        'url',
        type=str,
        help='Room IDを含む完全なURL'
    )
    parser.add_argument(
        '--ws-host',
        type=str,
        default='localhost',
        help='WebSocketサーバーのホスト名 (デフォルト: localhost)'
    )
    parser.add_argument(
        '--ws-port',
        type=int,
        default=1234,
        help='WebSocketサーバーのポート番号 (デフォルト: 1234)'
    )
    
    return parser.parse_args()

async def main() -> None:
    """
    メイン処理を実行
    
    WebSocketサーバーに接続し、JSONファイルからノードとエッジのデータを
    読み込んで表示します。
    """
    # コマンドライン引数の解析
    args = parse_arguments()
    
    try:
        # URLからRoom IDを抽出
        room_id = extract_room_id(args.url)
        websocket_url = f"ws://{args.ws_host}:{args.ws_port}/graph-collab-{room_id}"
        
        print(f"Connecting to: {websocket_url}")
        print(f"Using input file: {args.input_file}")
            
        # JSONファイルの存在確認
        if not args.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {args.input_file}")
            
        # Yjsドキュメントを作成
        ydoc = Y.YDoc()
        
        # WebSocketサーバーに接続
        async with (
            connect(websocket_url) as websocket,
            WebsocketProvider(ydoc, websocket)
        ):
            await asyncio.sleep(1)
            
            # 'nodes'と'edges'というYMapを取得または作成
            ymap_nodes = ydoc.get_map("nodes")
            ymap_edges = ydoc.get_map("edges")
            await asyncio.sleep(1)
            
            # グラフ表示の初期化
            with ydoc.begin_transaction() as t:
                for key in list(ymap_nodes.keys()):
                    ymap_nodes.pop(t, key=key)
                for key in list(ymap_edges.keys()):
                    ymap_edges.pop(t, key=key)
            await asyncio.sleep(1)
            
            print(f"\n-----")
            await asyncio.sleep(1)
            
            # JSONファイルから新しいノードデータを読み込む
            try:
                with args.input_file.open('r', encoding='utf-8') as file:
                    read_data = json.load(file)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON format in file: {args.input_file}")
            
            # トランザクションを開始してYMapにデータを追加（更新）
            with ydoc.begin_transaction() as t:
                for node in read_data['nodes']:
                    new_node = generate_node_data(
                        id=node['id'],
                        label=node['label'],
                        x=node['position_x'],
                        y=node['position_y'],
                        editor_name="LLM",
                        width=node['width'],
                        height=node['height'],
                        creator_editor_id_suffix="LLM",
                        node_type=node['nodeType']
                    )
                    ymap_nodes.set(t, new_node["id"], new_node)
                for edge in read_data['links']:
                    new_edge = generate_edge_data(
                        id=edge['id'],
                        label=edge['linkType'],
                        source=edge['source'],
                        target=edge['target'],
                        editor_name="LLM",
                        creator_editor_id_suffix="LLM"
                    )
                    ymap_edges.set(t, new_edge["id"], new_edge)
                
            await asyncio.sleep(1)

            # 'nodes'と'edges'というYMapを取得または作成
            ymap_nodes = ydoc.get_map("nodes")
            ymap_edges = ydoc.get_map("edges")

            # 辞書を作成
            nodes_dict = dict(ymap_nodes.items())
            edges_dict = dict(ymap_edges.items())

            await asyncio.sleep(1)

            # 辞書をJSON文字列に変換（エスケープなし）
            nodes_json = json.dumps(nodes_dict, indent=2, ensure_ascii=False)
            edges_json = json.dumps(edges_dict, indent=2, ensure_ascii=False)
            print(f"Nodes (JSON):\n{nodes_json}\nEdges (JSON):{edges_json}\n----")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    # asyncioのイベントループを実行
    asyncio.run(main())
