import AppMain from "@/components/layout/AppMain";
import Player from "@/components/Player";
import Queue from "@/components/Queue";

const MainPage = () => {
  return (
    <AppMain>
      <div className="flex flex-col gap-10">
        <Queue />
        <Player />
      </div>
    </AppMain>
  );
};

export default MainPage;
