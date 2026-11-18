from pathlib import Path
from staticsites.snapshots import Snapshotter
SNAPSHOT = Snapshotter(Path(__file__).resolve().parent.parent)
if __name__ == "__main__":
    SNAPSHOT.main()
