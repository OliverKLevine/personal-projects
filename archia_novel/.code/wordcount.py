import re
import string
import glob
import sys

def count(text):
    lowercase = set(string.ascii_lowercase)
    words = [word for word in re.sub('([!?";:\/\-\,\.])'," ",text.replace("*","")).split() if len(set(word.lower()).intersection(lowercase)) > 0]
    return len(words)


def propertize(text):
    
    text = re.sub('(\*\(\))',"",text.lower()).strip().split()

    words_to_remove = ["and"]
    text = [word for word in text if not word in words_to_remove]

    return "_".join(text)

def linked_name(text):
    f = lambda x: x.split("[[")[-1].split("|")[0].split("]]")[0]
    if type(text) is str and len(text.split("[[")) > 2: text = text.strip().split("[[")
    if type(text) is str: return f(text.strip())
    return [f(i) for i in text]

class Character:
    def __init__(self, novel, file):
        self.file = file
        self.name = file.split("/")[-1].split(".md")[0]
        if len(self.name.split()) == 1:
            self.link = f"[[{self.name}]]"
        else: self.link = f"[[{self.name}|{self.name.split()[0]}]]"
        with open(self.file) as fin:
            self.text = fin.read()
        for line in self.text.split("\n"):
            if line[:2] == "**" and ":**" in line:
                property_name = propertize(line.split("**")[1].rsplit(":",1)[0])
                if "summary" in property_name:
                    property_name = property_name.split("_summary")[0].split("_")[-1] + "_summary"
                self.__dict__[property_name] = line.split(":**")[1].strip()
            elif not line.strip(): property_name = None
            else:
                try: self.__dict__[property_name] += line
                except: pass

    def search(self):
        self.find_scenes()
    
    def find_scenes(self):
        self.cannonical_scenes = [self.novel.find_scene(scene) for scene in linked_name(self.cannonical_scenes) if scene.strip()]
        self.scratch_scenes = [self.novel.find_scene(scene, cannonical_only=False) for scene in linked_name(self.scratch_scenes) if scene.strip()]
        self.scenes = self.cannonical_scenes + self.scratch_scenes

class Scene:
    def __init__(self, novel, file):
        self.file = file
        self.name = file.split("/")[-1].split(".md")[0]
        self.link = f"[[{self.name}]]"
        with open(self.file) as fin:
            self.text = fin.read()
        if len(self.text.split("---\n")) < 2:
            vault = self.file.rsplit("/",1)[0]
            print(vault)
            with open(f"{vault}/templates/Scene.md") as fin:
                template = fin.read()
                self.text = template + self.text
            with open(self.file,"w") as fo:
                fo.write(self.text)
        self.header = self.text.split("---\n")[1]
        self.text = self.text.split("---\n",2)[-1]
        for line in self.header.split("\n"):
            if ":" in line:
                self.__dict__[propertize(line.split(":")[0])] = line.split(":",1)[1]
        self.chapter = int(self.chapter)
        if "cannonical" in self.file: self.cannonical = True
        else: self.cannonical = False
        self.word_count = count(self.text)
        self.description_link = f"[[{self.name}|{self.short_description}]]"
    
    def search(self):
        self.find_characters()
        self.linking_scenes()
    
    def find_characters(self):
        if self.characters:
            self.characters = [self.novel.find_character(name) for name in linked_name(self.characters)]
    
    def linking_scenes(self):
        is_scene = lambda x: x.strip() and not x.lower().strip() == "n/a"
        if is_scene(self.previous_scene): 
            self.previous_scene = self.novel.find_scene(self.previous_scene)
        else: self.previous_scene = None
        if is_scene(self.next_scene):
            self.next_scene = self.novel.find_scene(self.next_scene)
        else: self.next_scene = None

class Chapter:
    def __init__(self, novel, number):
        self.number = int(number)
        self.novel = int(novel)
        self.scenes = []
        self.characters = []
        self.word_count = 0
        unordered_scenes = [scene for scene in self.novel if scene.chapter == self.number]
        if unordered_scenes:
            #order scenes
            self.scenes = [unordered_scenes.pop(0)]
            while unordered_scenes:#TODO test this later
                n_scenes = len(self.scenes)
                for i in range(n_scenes):
                    if self.scenes[i].previous_scene in unordered_scenes:
                        self.scenes.insert(self.scenes[i].previous_scene,i)
                        unordered_scenes.remove(self.scenes[i].previous_scene)
                        break
                    if self.scenes[i].next_scene in unordered_scenes:
                        self.scenes.insert(self.scenes[i].next_scene,i+1)
                        unordered_scenes.remove(self.scenes[i].next_scene)
                        break
                if n_scenes == len(self.scenes) and unordered_scenes:
                    print(f"Error: non-adjacent scenes in chapter {self.number}",file=sys.stderr)
                    quit(1)

            #get list of characters
            self.characters = set([character for scene in self.scenes for character in scene.characters])
            #order list of characters
            self.characters = [character for character in self.novel.characters if character in self.characters]

            #get word count
            self.word_count = sum([scene.word_count for scene in self.scenes])

        #get title
        self.title = self.novel.table[self.number]["title"]
    
    def table_row(self, header):
        data = {
            "chapter": str(self.number),
            "title": self.title,
            "scenes": ", ".join([scene.link for scene in self.scenes]),
            "characters": ", ".join([character.link for character in self.characters]),
            "word_count": {True:str(self.word_count),False:""}[bool(self.word_count)]
        }
        return " | ".join([""] + [data[i].strip() for i in header] + [""]).strip()

class Novel:
    def __init__(self, vault):
        self.vault = vault
        self.characters = [Character(self, file) for file in glob.glob(f"{vault}/characters/*")]
        self.cannonical_scenes = [Scene(self, file) for file in glob.glob(f"{vault}/scenes_cannonical/*")]
        self.scratch_scenes = [Scene(self, file) for file in glob.glob(f"{vault}/scenes_scratch/*")]
        self.scenes = self.cannonical_scenes + self.scratch_scenes
        self.get_table()
        self.chapters = [Chapter(self,number) for number in range(1,26)]
    
    def find_scene(self, search_term, cannonical_only=True):
        search_term = linked_name(search_term)
        if cannonical_only:
            return [scene for scene in self.cannonical_scenes if scene.name == search_term][0]
        else:
            return [scene for scene in self.scenes if scene.name == search_term][0]
    
    def find_character(self, name, all=False):
        name = linked_name(name)
        characters = [character for character in self.characters if name in character.name]
        if all: return characters
        return characters[0]
    
    def get_table(self):
        if "table" in self.__dict__: return self.table
        characters = self.characters
        table_file = f"{self.vault}/outline/table.md"
        with open(table_file) as fin:
            table = fin.read()
        table = [[i.strip() for i in line.split("|")] for line in table.split("\n") if "|" in line]
        self.table_header = header = [propertize(i) for i in table.pop(0)]
        self.table = [table[0]] + [{header[i]:line[i] for i in range(1,len(header)-1)} for line in table[1:]]
        return self.table
    
    def update_table(self):
        if not "table" in self.__dict__: self.get_table()
        table_file = f"{self.vault}/outline/table.md"
        table = "\n".join([chapter.table_row(self.table_header) for chapter in self.chapters])
        if "--debug" in sys.argv:
            print(table)
        else:
            with open(table_file,"w") as fo:
                fo.write(table)
    
    def update_outline(self):
        if not "chapter_info" in self.__dict__: self.get_table()
        with open(f"{self.vault}/outline/Overview.md","w") as fo:
            for chapter in self.chapters:
                if chapter.scenes:
                    content = [f"### Chapter {chapter.number}: {chapter.title}"] + [scene.description_link for scene in chapter.scenes] + [""]
                    fo.write("\n".join(content))

def main():
    vault = __file__.split("/.code")[0]
    novel = Novel(vault)
    novel.update_table()
    novel.update_outline()


if __name__ == "__main__":
    main()