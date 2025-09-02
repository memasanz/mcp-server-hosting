"""PowerPoint operations client for blob storage and HTTP requests."""

from typing import Any
import httpx
from azure.storage.blob import BlobClient
from azure.core.exceptions import AzureError
import os
import tempfile
from urllib.parse import urlparse

# Configure timeouts
HTTP_TIMEOUT = httpx.Timeout(
    connect=10.0,    # Connection timeout
    read=120.0,     # Read timeout for larger files
    write=60.0,     # Write timeout
    pool=180.0      # Pool timeout
)

BLOB_TIMEOUT = 180  # 180 seconds timeout for blob operations

async def fetch_file(url: str) -> bytes | None:
    """Fetch a file from a URL with proper timeout handling."""
    # Clean up the URL and remove any newlines or extra whitespace
    url = url.strip().replace('\n', '').replace('\r', '')
    
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        try:
            # Create a client with URL encoding disabled for the path
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.content
        except httpx.TimeoutException:
            print(f"Timeout while fetching {url}")
            return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

async def download_pptx_to_temp(url: str) -> tuple[str | None, str | None]:
    """
    Downloads a PowerPoint file from a URL to a temporary file.
    
    Args:
        url (str): URL to the PowerPoint file
        
    Returns:
        tuple[str | None, str | None]: (local_path, error_message)
    """
    try:
        # Clean up the URL and remove any newlines or extra whitespace
        url = url.strip().replace('\n', '').replace('\r', '')
        
        # Parse the URL to get the blob name for creating temp file
        parsed_url = urlparse(url)
        blob_name = os.path.basename(parsed_url.path)
        
        # Create a temp file to download the PowerPoint
        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as temp_file:
            local_path = temp_file.name
            
        print(f"Downloading PowerPoint from URL: {blob_name}")
        
        # Download the file
        content = await fetch_file(url)
        if content is None:
            return None, "Failed to download PowerPoint file"
            
        with open(local_path, 'wb') as f:
            f.write(content)
        
        print(f"PowerPoint downloaded to: {local_path}")
        return local_path, None
        
    except Exception as e:
        error_msg = f"Error downloading PowerPoint: {str(e)}"
        print(error_msg)
        return None, error_msg

async def upload_pptx_to_blob(local_path: str, dest_url: str) -> tuple[bool, str | None]:
    """
    Uploads a PowerPoint file to blob storage.
    
    Args:
        local_path (str): Path to the local PowerPoint file
        dest_url (str): Destination blob URL with SAS token
        
    Returns:
        tuple[bool, str | None]: (success, error_message)
    """
    try:
        # Parse the destination URL
        parsed_dest = urlparse(dest_url)
        if not parsed_dest.netloc:
            return False, "Invalid destination URL"
        
        # Set up blob client with timeout
        blob_client = BlobClient.from_blob_url(dest_url, timeout=BLOB_TIMEOUT)
        
        # Upload the file to blob storage
        with open(local_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            
        print(f"Presentation uploaded to: {dest_url}")
        return True, None
        
    except AzureError as e:
        error_msg = f"Azure storage error: {str(e)}"
        print(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error uploading to blob storage: {str(e)}"
        print(error_msg)
        return False, error_msg

def cleanup_temp_file(file_path: str) -> None:
    """
    Safely deletes a temporary file.
    
    Args:
        file_path (str): Path to the file to delete
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        print(f"Warning: Error during cleanup of temporary file: {e}")
