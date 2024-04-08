import React, { useState, useEffect } from "react";
import { IPerson } from "../schemas/IData";

interface IProps {
  data: IPerson[] | any;
  prevPhoneNumbers: Record<number, number>;
}

const TableComponent: React.FC<IProps> = ({ data, prevPhoneNumbers }) => {
  const [primaryPerson, setPrimaryPerson] = useState<
    Record<number, IPerson["phone_numbers"][0] | null>
  >({});

  useEffect(() => {
    const updatePrimaryForPerson = (person: IPerson) => {
      setPrimaryPerson((prevPrimary) => ({
        ...prevPrimary,
        [person.id]:
          person.phone_numbers.find((phone) => phone.is_primary) || null,
      }));
    };

    data.forEach(updatePrimaryForPerson);
  }, [data]);

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse table-auto">
        <thead className="bg-gray-800 text-white">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
              Имя
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
              Фамилия
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
              Основной номер
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
              Доп. номер
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((person: IPerson, index: number) => (
            <tr
              key={index}
              className={`${
                index % 2 === 0 ? "bg-gray-100" : "bg-white"
              } border-b border-gray-200`}>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className="text-sm font-medium text-gray-900">
                  {person.name}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className="text-sm font-medium text-gray-900">
                  {person.surname}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className="text-sm font-medium text-gray-900">
                  {primaryPerson?.[person.id]?.country_code}
                  {primaryPerson?.[person.id]?.number || (
                    <span className="text-red-500">Нет основного номера</span>
                  )}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                {person.phone_numbers.find((phone) => !phone.is_primary)
                  ?.country_code ? (
                  <span className="text-sm font-medium text-gray-900">
                    {
                      person.phone_numbers.find((phone) => !phone.is_primary)
                        ?.country_code
                    }
                    {
                      person.phone_numbers.find((phone) => !phone.is_primary)
                        ?.number
                    }
                  </span>
                ) : (
                  <span className="text-sm font-medium text-gray-900 text-red-500">
                    Доп. номер отсутствует
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
