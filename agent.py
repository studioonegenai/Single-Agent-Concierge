# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.§

"""Agent module for the Civics Concierge."""

import logging
import warnings
from google.adk.agents import Agent  # 2026 Best Practice
from config.config import Config
from prompts.prompts import GLOBAL_INSTRUCTION, INSTRUCTION

# Import your new municipal logic
from tools.civics_tools import ( 
    check_zoning_rules,
    access_service_queue,
    schedule_city_inspection,
    generate_permit_qr,
    send_call_companion_link
)

# Standardized Callback Signatures
from shared_libraries.callbacks import (
    rate_limit_callback, # maps to before_model_callback
    before_agent,
    before_tool,
    after_tool
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")
logger = logging.getLogger(__name__)

# Initialize Agent
civics_agent = Agent(
    name="CivicsConcierge",
    model="gemini-3-flash-preview", # 2026 performance model
    instruction=f"{GLOBAL_INSTRUCTION}\n\n{INSTRUCTION}", # Combined for context depth
    tools=[
        check_zoning_rules,
        access_service_queue,
        schedule_city_inspection,
        generate_permit_qr,
        send_call_companion_link
    ],
    # Callback Hooks
    before_agent_callback=before_agent,
    before_model_callback=rate_limit_callback,
    before_tool_callback=before_tool,
    after_tool_callback=after_tool
)

output_key="concierge_output", # Saves final response to session state
root_agent = civics_agent

if __name__ == "__main__":
    print(f"Successfully initialized agent: {civics_agent.name} using model {civics_agent.model}")
