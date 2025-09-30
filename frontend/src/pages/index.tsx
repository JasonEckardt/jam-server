import Player from "@/components/Player";
import Queue from "@/components/Queue";

const MainPage = () => {
  return (
    <div className="flex flex-col gap-10">
      <Queue />
      <Player />
    </div>
  );
};

export default MainPage;
