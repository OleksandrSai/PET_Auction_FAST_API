export  interface UserBase {
  login: string;
}
export interface UserAuth extends UserBase{
  password: string;
}

export interface UserBids extends UserBase{
  password: string;
  id: number;
  name: string;
}
