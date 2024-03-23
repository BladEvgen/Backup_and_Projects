import App from "..";
import * as bases from "../components/bases";

export default function Page() {
  return (
    <bases.Base2>
      <p className="text-warning">HOME PAGE</p>
      <div className={"text-white "}>
        <App />
      </div>
    </bases.Base2>
  );
}
