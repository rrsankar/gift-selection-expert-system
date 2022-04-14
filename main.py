from pyknow import *

toy_features = []
toy_feature_map = {}
toy_desc_map = {}


def preprocess():
    global toy_features, toy_desc_map

    toys_f = open("toy_names.txt")
    toys_t = toys_f.read()
    toys_list = toys_t.split("\n")
    toys_f.close()

    for toy_iter in toys_list:

        toy_feature_file = open("toy_features/" + toy_iter + ".txt")
        toy_features_read = toy_feature_file.read()
        toy_features_split = toy_features_read.split("\n")
        toy_features.append(toy_features_split)
        toy_feature_map[str(toy_features_split)] = toy_iter
        toy_feature_file.close()

        toy_desc_file = open("toy_descriptions/" + toy_iter + ".txt")
        toy_desc_read = toy_desc_file.read()
        toy_desc_map[toy_iter] = toy_desc_read
        toy_desc_file.close()


def get_description(toy):
    return toy_desc_map[toy]


def if_not_matched(toy):
    print("")
    id_toy = toy
    toy_details = get_description(id_toy)
    print("")
    print("The most probable toy that you can buy is %s\n" % id_toy)
    print("A short description of the toy is given below :\n")
    print(toy_details + "\n")


class Greetings(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        print("\nHi, I am your toy specialist. I will like to help you choose a toy.")
        print("Please answer a few questions, and I can help you out.")
        yield Fact(action="find_toy")

    # CHOICES

    @Rule(Fact(action='find_toy'), NOT(Fact(age=W())), salience=1)
    def choice_0(self):
        self.declare(Fact(age=input("\nAge:\n0-5, 5-10, 10-15 : ")))

    @Rule(Fact(action='find_toy'), NOT(Fact(gender=W())), salience=1)
    def choice_1(self):
        self.declare(Fact(gender=input("\nGender:\n(male/female) : ")))

    @Rule(Fact(action='find_toy'), NOT(Fact(toy_type=W())), salience=1)
    def choice_2(self):
        self.declare(Fact(toy_type=input("\nToy Type:\n(A: Action Figure/ O: Outdoors) : ")))

    # TOYS

    @Rule(Fact(action='find_toy'), Fact(toy_type="A"), Fact(age="0-5"), Fact(gender="male"))
    def toy_0(self):
        self.declare(Fact(toy="Fake_Bugs"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="A"), Fact(age="0-5"), Fact(gender="female"))
    def toy_1(self):
        self.declare(Fact(toy="Squishy_Toys"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="A"), Fact(age="5-10"), Fact(gender="male"))
    def toy_2(self):
        self.declare(Fact(toy="Pokemon_Charizard"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="A"), Fact(age="5-10"), Fact(gender="female"))
    def toy_3(self):
        self.declare(Fact(toy="Nintendo_Kirby"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="A"), Fact(age="10-15"), Fact(gender="male"))
    def toy_4(self):
        self.declare(Fact(toy="Toys_Batman"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="A"), Fact(age="10-15"), Fact(gender="female"))
    def toy_5(self):
        self.declare(Fact(toy="Star_Wars"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="O"), Fact(age="0-5"), Fact(gender="male"))
    def toy_6(self):
        self.declare(Fact(toy="nerf_gun"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="O"), Fact(age="0-5"), Fact(gender="female"))
    def toy_7(self):
        self.declare(Fact(toy="Inflatable_bouncer"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="O"), Fact(age="5-10"), Fact(gender="male"))
    def toy_8(self):
        self.declare(Fact(toy="pool"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="O"), Fact(age="5-10"), Fact(gender="female"))
    def toy_9(self):
        self.declare(Fact(toy="Exercise_Hoops"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="O"), Fact(age="10-15"), Fact(gender="male"))
    def toy_10(self):
        self.declare(Fact(toy="Karaoke_Microphone"))

    @Rule(Fact(action='find_toy'), Fact(toy_type="O"), Fact(age="10-15"), Fact(gender="female"))
    def toy_11(self):
        self.declare(Fact(toy="pool"))

    @Rule(Fact(action='find_toy'), Fact(toy=MATCH.toy), salience=-998)
    def toy(self, toy):
        print("")
        id_toy = toy
        toy_details = get_description(id_toy)
        print("")
        print("The most probable toy that you can buy is %s\n" % id_toy)
        print("A short description of the toy is given below :\n")
        print(toy_details + "\n")

    @Rule(Fact(action='find_toy'),
          Fact(age=MATCH.age),
          Fact(gender=MATCH.gender),
          Fact(toy_type=MATCH.toy_type),
          NOT(Fact(toy=MATCH.toy)), salience=-999)
    def not_matched(self):
        print("\nUnfortunately, the system did not find any toy that matches your requirements.")


if __name__ == "__main__":
    preprocess()
    engine = Greetings()
    while True:
        engine.reset()  # Prepare the engine for the execution.
        engine.run()  # Run it!
        print("\nWould you like to get another recommendation? [y: yes | n: no]")
        if input() in ["n", "no"]:
            exit()
