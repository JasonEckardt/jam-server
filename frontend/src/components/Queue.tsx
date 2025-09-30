import useQueue from "@/hooks/useQueue";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

const Queue = () => {
  const { url, queue, setUrl, handleAddTrack } = useQueue();

  console.log(queue);

  return (
    <div className="flex max-w-4xl gap-2">
      <Input type="text" placeholder="Enter the song URL" defaultValue={url} onBlur={(e) => setUrl(e.target.value)} />
      <Button className="bg-green-500" onClick={handleAddTrack}>
        Add to Queue
      </Button>
    </div>
  );
};

export default Queue;
