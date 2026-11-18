import enum
import logging

from livekit.agents import Agent, function_tool

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)


class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"


class AssistantFnc(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful voice assistant created with LiveKit. "
                "You can check and change the temperature in different rooms. "
                "Use the available tools whenever the user asks about room "
                "temperature or wants to change it. "
                "Keep your spoken responses short and concise."
            )
        )

        self.temperature = {
            Zone.LIVING_ROOM: 22,
            Zone.BEDROOM: 20,
            Zone.KITCHEN: 24,
            Zone.BATHROOM: 23,
            Zone.OFFICE: 21,
        }

    @function_tool()
    async def get_temperature(self, zone: str) -> str:
        """Get the current temperature in a specific room.

        Args:
            zone: The room name. Use living_room, bedroom, kitchen,
                bathroom, or office.
        """
        try:
            selected_zone = Zone(zone.lower())
        except ValueError:
            return (
                "Invalid room. Available rooms are: living_room, "
                "bedroom, kitchen, bathroom, and office."
            )

        temp = self.temperature[selected_zone]

        logger.info("Get temperature - zone: %s", zone)

        return (
            f"The temperature in the {zone} "
            f"is {temp} degrees Celsius."
        )

    @function_tool()
    async def set_temperature(self, zone: str, temp: int) -> str:
        """Set the temperature in a specific room.

        Args:
            zone: The room name. Use living_room, bedroom, kitchen,
                bathroom, or office.
            temp: The new temperature in degrees Celsius.
        """
        try:
            selected_zone = Zone(zone.lower())
        except ValueError:
            return (
                "Invalid room. Available rooms are: living_room, "
                "bedroom, kitchen, bathroom, and office."
            )

        self.temperature[selected_zone] = temp

        logger.info(
            "Set temperature - zone: %s, temperature: %s",
            zone,
            temp,
        )

        return (
            f"The temperature in the {zone} "
            f"is now {temp} degrees Celsius."
        )
