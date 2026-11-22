from dataclasses import dataclass
from drafter import *


@dataclass
class Constellation:
    date_label: str
    name: str
    info: str

@dataclass
class State:
    user_name: str
    birth_month: str
    birth_day: int
    saved_skies: list[Constellation]
    error_message: str

def build_constellation(month: str, day: int) -> Constellation:
    date_label = month + " " + str(day)
    if month == "January" and day == 1:
        return Constellation(
            date_label,
            "Orion (New Year Sky)",
            "Sirius, the brightest star in the sky, shines on January 1.",)
    if (month == "December" and day >= 22) or (month == "January" and day <= 19):
        return Constellation(
            date_label,
            "Capricorn",
            "Known as the Sea Goat, positioned in the southern autumn or winter sky.",)
    if (month == "January" and day >= 20) or (month == "February" and day <= 18):
        return Constellation(
            date_label,
            "Aquarius",
            "Pictured as a Water Bearer, stretching across the southern sky.",)
    if (month == "February" and day >= 19) or (month == "March" and day <= 20):
        return Constellation(
            date_label,
            "Pisces",
            "Represents two fish and sits near the vernal equinox point.",)
    if (month == "March" and day >= 21) or (month == "April" and day <= 19):
        return Constellation(
            date_label,
            "Aries",
            "Known as the Ram, located in the northern spring/autumn sky.",)
    if (month == "April" and day >= 20) or (month == "May" and day <= 20):
        return Constellation(
            date_label,
            "Taurus",
            "Home to the bright star Aldebaran and the Pleiades star cluster.",)
    if (month == "May" and day >= 21) or (month == "June" and day <= 20):
        return Constellation(
            date_label,
            "Gemini",
            "Marked by twin bright stars, Castor and Pollux.",)
    if (month == "June" and day >= 21) or (month == "July" and day <= 22):
        return Constellation(
            date_label,
            "Cancer",
            "Pictured as a crab, holding the Beehive Cluster.",)
    if (month == "July" and day >= 23) or (month == "August" and day <= 22):
        return Constellation(
            date_label,
            "Leo",
            "Pictured as a lion, features a distinct sickle shape.",)
    if (month == "August" and day >= 23) or (month == "September" and day <= 22):
        return Constellation(
            date_label,
            "Virgo",
            "Represented by the Maiden, anchored by Spica, one of the brightest stars in the night sky.",)
    if (month == "September" and day >= 23) or (month == "October" and day <= 22):
        return Constellation(
            date_label,
            "Libra",
            "The only constellation shaped like an inanimate object: the scales.",)
    if (month == "October" and day >= 23) or (month == "November" and day <= 21):
        return Constellation(
            date_label,
            "Scorpio",
            "Represented by a Scorpion, and features the bright reddish star Antares.",)
    return Constellation(
        date_label,
        "Sagittarius",
        "Often pictured as an archer and centuar, pointing toward the center of the Milky Way.",)

def format_saved_list(saved_skies: list[Constellation]) -> list:
    items = []
    for entry in saved_skies:
        line = entry.date_label + " - " + entry.name + ": " + entry.info
        items.append(BulletedList([line]))
    return items


@route
def index(state: State) -> Page:
    return Page(
        state,
        [
            Header("Birthday Night Sky"),
            "Discover constellations tied to your birthday and save your results.",
            Button("Enter Your Birthday", input_page),
            Button("View Saved Results", saved_results),
        ],)


@route
def input_page(state: State) -> Page:
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",]
    days = [str(day_num) for day_num in range(1, 32)]
    content = [
        Header("Tell Us About Your Birthday"),
        TextBox("name_input", state.user_name),
        SelectBox("month_input", months, state.birth_month),
        SelectBox("day_input", days, str(state.birth_day)),
        Button("Show My Sky", submit_sky),
        Button("Back Home", index),]
    if state.error_message != "":
        content.insert(1, state.error_message)
    return Page(state, content)


@route
def submit_sky(state: State, name_input: str, month_input: str, day_input: str) -> Page:
    cleaned_name = name_input.strip()
    if cleaned_name == "":
        state.error_message = "Please enter your name before continuing."
        return input_page(state)
    state.error_message = ""
    state.user_name = cleaned_name
    state.birth_month = month_input
    state.birth_day = int(day_input)
    constellation = build_constellation(state.birth_month, state.birth_day)

    return Page(
        state,
        [
            Header(state.user_name + "'s Night Sky"),
            "Exact Birthday: " + state.birth_month + " " + str(state.birth_day),
            "Featured Constellation: " + constellation.name,
            constellation.info,
            Button("Save This Result", save_result),
            Button("Next: Star Facts", conclusion_page),
            Button("Change Birthday", input_page),
        ],)

@route
def save_result(state: State) -> Page:
    new_entry = build_constellation(state.birth_month, state.birth_day)
    state.saved_skies.append(new_entry)
    return saved_results(state)


@route
def saved_results(state: State) -> Page:
    body = [Header("Saved Birthday Skies")]
    if len(state.saved_skies) == 0:
        body.append("No saved results yet. Generate a sky to save one!")
    else:
        body.extend(format_saved_list(state.saved_skies))
        body.append(Button("Clear Saved Results", clear_saved))
    body.append(Button("Enter Another Birthday", input_page))
    body.append(Button("Back Home", index))
    return Page(state, body)


@route
def clear_saved(state: State) -> Page:
    state.saved_skies = []
    return saved_results(state)


@route
def conclusion_page(state: State) -> Page:
    greeting = state.user_name if state.user_name != "" else "stargazer"
    return Page(
        state,
        [
            Header("Wrapping Up Your Sky Tour"),
            "Thanks for exploring the night sky, " + greeting + "!",
            "Star Fact: Light from the stars you see at night can take years to reach Earth.",
            "Star Fact: Earth's tilt is why different constellations stand out across seasons.",
            Button("Start Over", index),
        ],)


start_server(
    State(
        user_name="",
        birth_month="January",
        birth_day=1,
        saved_skies=[],
        error_message="",
    ))
