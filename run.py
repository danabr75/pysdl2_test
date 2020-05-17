# FIRST TIME: INSTALL pipenv
# pipenv install 
# pipenv shell
# python run.py

from main import MainEngine
from models.scene_base import SceneBase
from models.rouge_like import RogueLike

# if __name__ == "__main__":
#   MainEngine().main()

if __name__ == '__main__':
    # example, with a borderless yet ugly green window
    m = MainEngine()
    m.set_scene(scene=RogueLike)
    m.run()