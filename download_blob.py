import os
from azure.storage.blob import BlobServiceClient

# 1. Azure Blob 連線資訊
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=healthy;AccountKey=/KaT8yQ461o3B4TWUDNhRingFu28EO70b53PWHzMeiQ5js9MFgDTBNW+7xER5vm3sQDe+R9j5hyR+AStS50GLQ==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "hhh"

# 2. 檔案下載目錄（自行修改）
DOWNLOAD_FOLDER = "downloaded_images"

def download_and_delete_blobs():
    """
    從指定 Azure Blob 容器中下載所有圖片到本機，再刪除遠端的 Blob。
    下載完之後，本機會保留下載的檔案，而雲端上的 Blob 被刪除。
    """
    # 建立 BlobServiceClient 與 ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # 若本機尚未有指定下載資料夾，先建立
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    # 列出容器內所有的 Blob
    blob_list = container_client.list_blobs()

    for blob in blob_list:
        # 取得該 blob 的 client
        blob_client = container_client.get_blob_client(blob.name)
        
        # 設定下載到本機的檔案路徑
        download_file_path = os.path.join(DOWNLOAD_FOLDER, blob.name)
        
        try:
            # 3. 下載 Blob 到本機
            print(f"正在下載 Blob：{blob.name}...")
            with open(download_file_path, "wb") as download_file:
                download_data = blob_client.download_blob()
                download_file.write(download_data.readall())
            print(f"下載完成：{download_file_path}")

            # 4. 刪除雲端上的 Blob
            blob_client.delete_blob()
            print(f"已從 Blob 刪除：{blob.name}")

        except Exception as e:
            print(f"處理檔案 {blob.name} 時發生錯誤：{e}")
            # 如需進一步錯誤處理，可在此添加重試或記錄機制

def main():
    download_and_delete_blobs()

if __name__ == "__main__":
    main()
