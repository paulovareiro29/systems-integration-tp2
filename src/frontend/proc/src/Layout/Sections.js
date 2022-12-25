import FilterByArea from "../Procedures/FilterByArea";
import FilterByType from "../Procedures/FilterByType";
import FullList from "../Procedures/FullList";

const Sections = [
  {
    id: "listing",
    label: "Full List",
    content: <FullList />,
  },
  {
    id: "filter-by-area",
    label: "Filter By Area",
    content: <FilterByArea />,
  },
  {
    id: "filter-by-type",
    label: "Filter By Type",
    content: <FilterByType />,
  },
];

export default Sections;
