interface IPhoneNumber {
  country_code: string;
  number: string;
  is_primary: boolean;
}

export interface IPerson {
  id: number;
  name: string;
  surname: string;
  phone_numbers: IPhoneNumber[];
}
