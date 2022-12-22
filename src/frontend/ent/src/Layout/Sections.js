import Airbnbs from "../Tables/Airbnbs";
import Areas from "../Tables/Areas";
import Hosts from "../Tables/Hosts";
import Types from "../Tables/Types";

const Sections = [
  {
    id: "hosts",
    label: "Hosts",
    content: <Hosts />,
  },
  {
    id: "types",
    label: "Types",
    content: <Types />,
  },
  {
    id: "areas",
    label: "Areas",
    content: <Areas />,
  },
  {
    id: "airbnbs",
    label: "Airbnbs",
    content: <Airbnbs />,
  },
];

export default Sections;
