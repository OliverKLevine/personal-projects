import re
import string
import glob
import sys

def count(file):
    lowercase = set(string.ascii_lowercase)
    with open(file,"r") as fin:
        ftext = fin.read().replace("*","")
        words = [word for word in re.sub('([!?";:\/\-\,\.])'," ",ftext).split() if len(set(word.lower()).intersection(lowercase)) > 0]
        return len(words)

def update_table(vault, characters):
    table_file = f"{vault}/outline/table.md"
    with open(table_file) as fin:
        table = fin.read()
    table = [[i.strip() for i in line.split("|")] for line in table.split("\n") if "|" in line]
    header = table.pop(0)
    table = [table[0]] + [{header[i]:line[i] for i in range(1,len(header)-1)} for line in table[1:]]
    header = header[1:-1]
    for chapter in range(1,len(table)):
        table[chapter]["Word Count"] = 0
        table[chapter]["Characters"] = []
        if "[[" in table[chapter]["Scenes"]:
            for scene in table[chapter]["Scenes"].split("[[")[1:]:
                scene_name = scene.split("]]")[0].split("|")[0]
                #Update wordcount
                scene_file = f"{vault}/scenes_cannonical/{scene_name}.md"
                table[chapter]["Word Count"] += count(scene_file)

                #Update characters in chapter
                for character in characters:
                    if scene_name in character.scenes:
                        table[chapter]["Characters"].append(character)
    chapter_info = []
    for chapter in range(1,len(table)):
        chapter_info.append(table[chapter].copy())
        if table[chapter]["Word Count"] == 0:
            table[chapter]["Word Count"] = ""
        table[chapter]["Characters"] = ", ".join([character.link.replace("|","\\|") for character in table[chapter]["Characters"]])
    table = [[""] + header + [""],table[0]] + [[""] + [line[key] for key in header] + [""] for line in table[1:]]
    table = [" | ".join([str(i) for i in line]).strip() for line in table]
    table = "\n".join(table)
    if "--debug" in sys.argv:
        print(table)
    else:
        with open(table_file,"w") as fo:
            fo.write(table)
    return chapter_info

class character:
    def __init__(self, file):
        self.file = file
        self.name = file.split("/")[-1].split(".md")[0]
        if len(self.name.split()) == 1:
            self.link = f"[[{self.name}]]"
        else: self.link = f"[[{self.name}|{self.name.split()[0]}]]"
        with open(self.file) as fin:
            self.text = fin.read()
        self.scenes = [scene.split("|")[0].split("]]")[0] for scene in self.text.split("**Canonical scenes:**")[1].split("\n")[0].split("[[") if scene.strip()]


def main():
    vault = __file__.split("/.code")[0]
    characters = [character(file) for file in glob.glob(f"{vault}/characters/*")]
    chapter_info = update_table(vault, characters)
    with open(f"{vault}/outline/Overview.md","w") as fo:
        for chapter in chapter_info:
            if chapter["Scenes"]:
                content = [f"### Chapter {chapter['Chapter']}: {chapter['Title']}"] + chapter["Scenes"].split(", ") + [""]
                fo.write("\n".join(content))


if __name__ == "__main__":
    main()