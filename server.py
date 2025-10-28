
# from nt import strerror
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
import json
import ssl
import urllib.request
from config import inforcer

// Create MCP Token Verifier
verifier = StaticTokenVerifier(
    tokens={
        inforcer.MCP_TOKEN: {
            "client_id": "testuser",
            "scopes": ["read:data", "write:data", "admin:users"]
        }
    },
    required_scopes=["read:data"]
)

// Create MCP Server, using the verifier
mcp = FastMCP("Inforcer MCP Server", auth=verifier)

// Add Inforcer API key to header
signed_header = {
        "Inf-Api-Key": f"{inforcer.INF_API_KEY}",
        "Content-Type": "application/json"
    }

@mcp.tool
def ping() -> str:
    """Ping: Ping the Inforcer MCP Server and return a validation of the MCP Token"""
    return f"Inforcer MCP Server is running, your id: {verifier.tokens[inforcer.MCP_TOKEN]['client_id']}"

@mcp.tool()
def get_tenants() -> dict:
    """Get Tenants: List and filter all tenants and return JSON"""

    url = (inforcer.INF_BASE_URL + "/tenants")          

    ssl_context = ssl.create_default_context()
    headers = signed_header

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            body = response.read()
    except Exception as exc:
        return {"error": str(exc)}

    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return {"raw": body.decode("utf-8", errors="replace")}


@mcp.tool()
def get_tenant_policies(client_Tenant_Id: int) -> dict:
    """Get Tenant Policies: Dive into tenant-level policies and return JSON"""

    url = (inforcer.INF_BASE_URL + "/tenants/" + str(client_Tenant_Id) + "/policies")          

    ssl_context = ssl.create_default_context()
    headers = signed_header

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            body = response.read()
    except Exception as exc:
        return {"error": str(exc)}

    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return {"raw": body.decode("utf-8", errors="replace")}

@mcp.tool()
def get_alignment_scores() -> dict:
    """Get Alignment Scores: Access alignment results and metrics and return JSON"""

    url = (inforcer.INF_BASE_URL + "/alignmentScores")          

    ssl_context = ssl.create_default_context()
    headers = signed_header

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            body = response.read()
    except Exception as exc:
        return {"error": str(exc)}

    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return {"raw": body.decode("utf-8", errors="replace")}

@mcp.tool()
def get_baselines() -> dict:
    """Get baselines: View baseline information and tenants assigned to that baseline and return JSON"""

    url = (inforcer.INF_BASE_URL + "/baselines")          

    ssl_context = ssl.create_default_context()
    headers = signed_header

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            body = response.read()
    except Exception as exc:
        return {"error": str(exc)}

    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        return {"raw": body.decode("utf-8", errors="replace")}

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)


