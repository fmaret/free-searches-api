from pprint import pprint
from bs4 import BeautifulSoup
import requests
import unidecode

from app.anonymity import get_ip, get_new_proxies


def format_normal_google_result(result: BeautifulSoup):
    data = {}
    data["title"] = result.find("h3").text
    data["url"] = result.find("a")["href"]
    try:
        data["subtitle-1"] = result.find("div", {"data-content-feature": "1"}).text
    except:
        pass
    return data

def format_dictionary_google_result(result: BeautifulSoup):
    pass


def format_google_result(result: BeautifulSoup):
    try:
        return format_normal_google_result(result)
    except Exception as e:
        print("ERROR: ", e)
        return

def format_google_results(soup: BeautifulSoup):
    results = soup.find(id="search").find("div").find("div").find_all("div", recursive=False)
    output = []
    for result in results:
        output.append(format_google_result(result))
    return output


def get_total_result_and_time(text: str):
    words = " ".join(unidecode.unidecode(text).split(",")).split(" ")[1:]
    total = ""
    for word in words:
        try:
            int(word)
            total += word
        except:
            break
    time = ""
    for i, word in enumerate(words):
        if len(word)>0 and word[0] == "(":
            time = word[1:] + "." + words[i+1]
    return int(total), float(time)


def get_menu_items(soup: BeautifulSoup, gl="fr"):
    menu_items = soup.find_all(class_="hdtb-mitem")
    return [{
        "position": i+1,
        "title": menu_item.text,
        "link": "https://www.google.com"+menu_item.find("a")["href"] if menu_item.find("a") else None
    } for i, menu_item in enumerate(menu_items)]


def get_knowledge_graph(soup: BeautifulSoup):
    graph = soup.find(class_="osrp-blk")
    if not graph:
        return None
    infos = graph.find_all({"div", "h2"}, {"data-attrid": True})
    pprint(infos)
    output = {}
    print([info["data-attrid"] for info in infos])
    images = []
    data = []
    debug = {}
    if graph.find(class_="ab_button"):
        output["website"] = graph.find(class_="ab_button")["href"]
    for info in infos:
        id = info["data-attrid"]
        if id in ["image", "secondary image"]:
            images.append({
                "link": info.find("a")["href"],
                "source": info["data-lpage"]
            })
        elif id == "title":
            output["title"] = info.text
        elif id == "description":
            output["description"] = {
                "text": info.find("span").text,
                "source": info.find("a")["href"] if info.find("a") else None
            }
        elif id == "kc:/local:one line summary":
            output["oneLineSummary"] = info.text
        elif id == "kc:/local:located in":
            output["situation"] = {
                "name": info.find("a").text,
                "url": info.find("a")["href"]
            }
        elif id == "kc:/location/location:address":
            spans = info.find_all("span")
            output["address"] = {
                "address": spans[-1].text,
                "url": spans[0].find("a")["href"]
            }
        elif id == "kc:/location/location:hours":
            spans = info.find_all("span")
            output["hours"] = {
                "devNote": "WIP",
                "hours": spans[-1].text,
                "url": spans[0].find("a")["href"]
            }
        elif id == "kc:/collection/knowledge_panels/has_phone:phone":
            spans = info.find_all("span")
            output["phone"] = {
                "phone": spans[-1].text,
                "url": spans[0].find("a")["href"]
            }
        elif id == "kc:/collection/knowledge_panels/local_reviewable:star_score":
            output["rating"] = info.find("div", recursive=False).find("div", recursive=False).find("span", recursive=False).text
            output["totalReviews"] = info.find("a").find("span").text
        elif ":/" in id:
            try:
                spans = info.find_all("span")
                debug[":".join(spans[0].text.split(":")[:-1]).strip()] = spans[1].text
            except:
                print("error with "+ id)
    if images:
        output["inlineImages"] = images
    output["debug"] = debug
    # title = graph.find("h2").text
    # site = graph.find(class_="ab_button")["href"] if graph.find(class_="ab_button") else None
    # try:
    #     rating_line = graph.find("div", {"data-attrid": "kc:/collection/knowledge_panels/local_reviewable:star_score"})
    #     rating = rating_line.find("div", recursive=False).find("div", recursive=False).find("span", recursive=False).text
    #     total_reviews = rating_line.find("a").find("span").text
    # except:
    #     rating = None
    #     total_reviews = None
    # infos = soup.find(id="kp-wp-tab-overview").find("div").find("div").find("div").find("div").find("div").find("div").find_all("div", recursive=False)
    # print([info for info in infos])
    # output = {}
    # for info in infos:
    #     try:
    #         spans = info.find_all("span")
    #         if len(spans) != 1:
    #             output[spans[0].text] = spans[1].text
    #         else:
    #             output[spans[0].text] = info.find("a").text
    #     except:
    #         pass
    # output.update({
    #     "title": title,
    #     "headerImages": [],
    #     "website": site,
    #     "rating": rating,
    #     "totalReviews": total_reviews
    # })

    return output


def make_google_search(search):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    }
    url = f'https://www.google.com/search?q={search}'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    total_results, time = get_total_result_and_time(soup.find(id="result-stats").text)
    output = {
        "searchMetadata": {
            "googleUrl": url,
        },
        "searchInformation": {
            "organicResultsState": "Results for exact spelling",
            "queryDisplayed": search,
            "totalResults": total_results,
            "timeTakenDisplayed": time,
            "menuItems": get_menu_items(soup)
        },
        "knowledgeGraph": get_knowledge_graph(soup)
    }
    #output["results"] = format_google_results(soup)
    return output