import os
import requests
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.function_tool import FunctionTool

load_dotenv()

MAPS_API_KEY = os.getenv("MAPS_API_KEY")

def search_location(origin: str, destination: str, place_type: str = "restaurant") -> dict:
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": origin,
        "radius": 5000,
        "type": place_type,
        "key": MAPS_API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data["status"] == "OK":
        places = data["results"]
        return "\n".join([place["name"] for place in places])
    else:
        return f"Error fetching locations: {data['status']}"

def get_directions(origin: str, destination: str, mode: str = "driving") -> dict:
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": MAPS_API_KEY,
        "mode": mode
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data["status"] == "OK":
        directions = data["routes"][0]["legs"][0]["steps"]
        return "\n".join([step["html_instructions"] for step in directions])
    else:
        return f"Error fetching directions: {data['status']}"
    
    return data

root_agent = LlmAgent(
    tools=[
        FunctionTool(
            name="get_directions",
            description="Get directions between two locations using Google Maps API.",
            func=get_directions
        ),
        FunctionTool(
            name="search_location",
            description="Search for nearby places of a specific type using Google Maps API.",
            func=search_location
        )
    ],
    model="gemini-2.0-pro",
    name="Maps_Agent"
)
