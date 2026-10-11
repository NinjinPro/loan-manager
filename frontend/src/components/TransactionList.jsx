import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { json } from 'react-router-dom';

const fetchTransactions = async () => {
  const { data } = await apiClient('/transactions');
  return data;
};

export default function TransactionList() {
  const { data: transactions, isLoading, isError, error } = useQuery({
    queryKey: ['transactions'],
    queryFn: fetchTransactions,
  });

  if (isLoading) return <div>⏱️ Loading ledger records...</div>;
  if (isError) return <div>⚠️ Error fetching logs: {error.message}</div>;

  return (
    <div>
      <h3>Recent Financial Transactions</h3>
      <ul>
        {transactions.map((tx) => (
          <li key={tx.id} style={{ color: tx.type === 'expense' ? 'red' : 'green' }}>
            <strong>{tx.description}</strong>: ${tx.amount} 
            <small> (By User ID: {tx.personId}) </small>
          </li>
        ))}
      </ul>
    </div>
  );
}
