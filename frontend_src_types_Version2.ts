export interface Product {
  id: string;
  title: string;
  price: number;
  thumbnail?: string;
  link?: string;
  // Optional field for model prediction / score
  predicted_score?: number;
}