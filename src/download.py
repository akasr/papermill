import httpx
import tempfile
from pathlib import Path
from fastapi import UploadFile, HTTPException


async def download_file_from_url(url: str, timeout: int = 30) -> UploadFile:
    """
    Download a file from a URL and return it as an UploadFile object.
    
    Args:
        url: The URL to download from
        timeout: Timeout in seconds for the download (default: 30)
        
    Returns:
        UploadFile object containing the downloaded file
        
    Raises:
        HTTPException: If the download fails or times out
    """
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            # Extract filename from URL or Content-Disposition header
            filename = _extract_filename(url, response.headers)
            
            # Get content type from response headers
            content_type = response.headers.get("content-type", "application/octet-stream")
            
            # Create a temporary file
            suffix = Path(filename).suffix if filename else ""
            temp_file = tempfile.NamedTemporaryFile(
                mode='w+b',
                delete=False,
                suffix=suffix
            )
            
            # Write the downloaded content to the temp file
            temp_file.write(response.content)
            temp_file.seek(0)  # Reset file pointer to beginning
            
            # Create an UploadFile object
            upload_file = UploadFile(
                file=temp_file,
                filename=filename,
                headers={"content-type": content_type}
            )
            
            return upload_file
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail=f"Request timeout: Failed to download file from {url} within {timeout} seconds"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"HTTP error occurred: {e.response.status_code} - {e.response.reason_phrase}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Network error occurred while downloading: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during download: {str(e)}"
        )


def _extract_filename(url: str, headers: httpx.Headers) -> str:
    """
    Extract filename from URL or Content-Disposition header.
    
    Args:
        url: The URL the file was downloaded from
        headers: Response headers
        
    Returns:
        Extracted filename
    """
    # Try to get filename from Content-Disposition header
    content_disposition = headers.get("content-disposition", "")
    if content_disposition:
        parts = content_disposition.split("filename=")
        if len(parts) > 1:
            filename = parts[1].strip('"').strip("'")
            if filename:
                return filename
    
    # Fall back to extracting from URL
    path = Path(url.split("?")[0])  # Remove query parameters
    filename = path.name
    
    # If no filename can be extracted, use a default
    if not filename or filename == "/":
        filename = "downloaded_file"
    
    return filename

