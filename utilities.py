def get_search_string(member):
    search_string_prefix = "https://news.google.com/search?q="
    search_string_suffix = "&hl=en-US&gl=US&ceid=US%3Aen"
    name = f"{member['full_name']}"
    name_list = name.split(" ")
    separator = '%20'
    new_name = separator.join(name_list)
    search_string = f"{search_string_prefix}{new_name}{search_string_suffix}"
    return search_string
