import { Box } from "@mui/material";
import TableComponent from "../components/TableComponent.tsx";
import { useEffect, useState } from "react";
import { IData } from "../schemas/IData.ts";
import axios from "axios";
import { isDebug, apiUrl } from "../../apiConfig.ts";

const StaffPage = () => {
  const [data, setData] = useState<IData[]>([]);
  const [totalSum, setTotalSum] = useState<number>(0);

  const getData = async () => {
    try {
      const res = await axios.get(`${apiUrl}/api/contracts/`);
      setData(res.data.data);
    } catch (error) {
      if (isDebug) {
        console.error(`Error: ${error}`);
      }
    }
  };

  useEffect(() => {
    getData();
  }, []);

  useEffect(() => {
    if (data) {
      setTotalSum(
        data.reduce(
          (accumulator, row) => accumulator + parseFloat(row.total),
          0
        )
      );
    }
  }, [data]);

  return (
    <>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          flexDirection: "column",
          alignItems: "center",
          gap: "5px",
        }}>
        <TableComponent data={data} totalSum={totalSum} />
      </Box>
    </>
  );
};

export default StaffPage;
