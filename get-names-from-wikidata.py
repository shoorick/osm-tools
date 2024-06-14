import xml.etree.ElementTree as ET
import requests
import argparse
import sys


def get_wikidata_info(wikidata_id):
    """Get WikiData as JSON"""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Process OSM XML file and enrich with Wikidata information."
    )
    parser.add_argument("-i", "--input", type=str, help="Input XML file")
    parser.add_argument("-o", "--output", type=str, help="Output XML file")
    return parser.parse_args()


args = parse_args()

input_file = args.input if args.input else sys.stdin
output_file = args.output if args.output else sys.stdout

# Read and parse XML
tree = ET.parse(input_file)
root = tree.getroot()

for node in root.findall(".//node"):
    modified = 0

    wikidata_tag = node.find("tag[@k='wikidata']")
    if wikidata_tag is not None:
        wikidata_id = wikidata_tag.get("v")
        wikidata_info = get_wikidata_info(wikidata_id)

        if wikidata_info:
            entity = wikidata_info["entities"][wikidata_id]
            labels = entity.get("labels", {})
            sitelinks = entity.get("sitelinks", {})

            # Search name in labels
            for lang, data in labels.items():
                lang_tag = f"name:{lang}"
                if node.find(f"tag[@k='{lang_tag}']") is None:
                    new_tag = ET.SubElement(node, "tag")
                    new_tag.set("k", lang_tag)
                    new_tag.set("v", data["value"])
                    modified = 1

            # Search name in Wikipedia links
            for site, data in sitelinks.items():
                if site == "commonswiki":
                    continue
                if site.endswith("wiki"):
                    lang = site[:-4]  # cut off 'wiki'
                    wikipedia_tag = f"wikipedia:{lang}"
                    if node.find(f"tag[@k='{wikipedia_tag}']") is None:
                        new_tag = ET.SubElement(node, "tag")
                        new_tag.set("k", wikipedia_tag)
                        new_tag.set("v", data["title"])
                        modified = 1

                    lang_tag = f"name:{lang}"
                    if node.find(f"tag[@k='{lang_tag}']") is None:
                        new_tag = ET.SubElement(node, "tag")
                        new_tag.set("k", lang_tag)
                        new_tag.set("v", data["title"])
                        modified = 1

            if modified:
                node.set("action", "modify")


# Save changed XML file
tree.write(output_file, encoding="UTF-8", xml_declaration=True)
