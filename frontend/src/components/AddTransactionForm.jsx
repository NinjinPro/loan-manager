import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { json } from 'react-router-dom';

const createTransaction = async (newTx) => {
  const { data } = await apiClient('/transactions', JSON.stringify(newTx));
  return data;
};

export default function AddTransactionForm() {
  const queryClient = useQueryClient();
  
  const [tx, setTx] = useState({
    description: "",
    amount: null,
  });
  // const [description, setDescription] = useState('');
  // const [amount, setAmount] = useState('');

  // Define mutation lifecycle configuration
  const mutation = useMutation({
    mutationFn: createTransaction,
    onSuccess: () => {
      // CRITICAL: Tells TanStack Query that the old transaction list cache is now stale.
      // This forces the TransactionList component to automatically refetch fresh background data.
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      
      // Reset local inputs
      setTx({
        description: "",
        amount: null,
      })
        
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!tx.description || !tx.amount) return;

    mutation.mutate({
      description: tx.description,
      amount: parseFloat(tx.amount),
      type: 'expense',
      personId: 1, // hardcoded mock placeholder matching API contract
    });
  };

  const formStyle = {
      margin: '20px 0',
      padding: '15px',
      background: '#f9f9f9'
  }
    
  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h3>Log New Expense</h3>
        
      <input 
        type="text" 
        placeholder="e.g., Office Supplies" 
        value={tx.description} 
        onChange={(e) => setTx((tx) => ({ ...tx, description: e.target.value }))} 
      />
        
      <input 
        type="number" 
        placeholder="Amount ($)" 
        value={tx.amount} 
        onChange={(e) => setAmount((tx) => ({ ...tx, amount: e.target.value }))} 
      />
        
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Saving...' : 'Add Transaction'}
      </button>
        
      {mutation.isError && 
      	<p style={{ color: 'red' }}>
            Error: {mutation.error.message}
        </p>
      }
        
    </form>
  );
}
