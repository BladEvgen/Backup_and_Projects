import React, { useState, useEffect } from "react";
import { IPerson } from "../schemas/IData";
import TableComponent from "../components/TableComponent";

const MainPage = () => {
  const [data, setData] = useState<IPerson[] | any>([]);
  const [prevPhoneNumbers, setPrevPhoneNumbers] = useState<
    Record<number, number>
  >({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/api/get_person_info/"
        );
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const responseData = await response.json();
        setData(responseData);

        const newPrevPhoneNumbers: Record<number, number> = {};

        responseData.forEach((person: IPerson) => {
          newPrevPhoneNumbers[person.id] = person.phone_numbers.length;
        });
        setPrevPhoneNumbers(newPrevPhoneNumbers);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();

    return () => {
      const shouldRefetch = data.some((person: IPerson) => {
        const prevLength = prevPhoneNumbers[person.id] || 0;
        return prevLength !== person.phone_numbers.length;
      });

      if (shouldRefetch) {
        fetchData();
      }
    };
  }, [data]);

  return (
    <>
      <div className="container mx-auto p-4">
        <TableComponent data={data} prevPhoneNumbers={prevPhoneNumbers} />
      </div>
    </>
  );
};

export default MainPage;
