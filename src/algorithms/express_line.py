from graph.graph import Graph


def build_express_line():

    g = Graph()

    g.add_connection(
        "ایستگاه ترمینال مسافربری قم", "ایستگاه قلعه کامکار", 1.2, 3, directed=True
    )
    g.add_connection(
        "ایستگاه قلعه کامکار", "ایستگاه میدان کشاورز", 2.5, 5, directed=True
    )
    g.add_connection(
        "ایستگاه میدان کشاورز", "ایستگاه میدان مطهری", 6, 10, directed=True
    )
    g.add_connection(
        "ایستگاه میدان مطهری",
        "ایستگاه حرم مطهر حضرت معصومه (س)",
        1.5,
        4,
        directed=True,
    )
    g.add_connection(
        "ایستگاه حرم مطهر حضرت معصومه (س)",
        "ایستگاه ارگ سالاریه",
        1,
        3,
        directed=True,
    )
    g.add_connection(
        "ایستگاه ترمینال مسافربری قم", "ایستگاه میدان مطهری", 8, 15, directed=True
    )  # express shortcut

    return g