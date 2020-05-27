from django.urls import reverse
from menu import Menu, MenuItem

sharing_children = (
    MenuItem(
        "Request builder",
        reverse("admin:core_oaipmh_harvester_app_request_builder"),
        icon="magic",
    ),
    MenuItem(
        "Data providers",
        reverse("admin:core_oaipmh_harvester_app_registries"),
        icon="database",
    ),
)

Menu.add_item("admin", MenuItem("OAI PMH HARVESTER", None, children=sharing_children))
