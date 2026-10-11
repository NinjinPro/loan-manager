import React, { useState } from 'react';
import TransactionList from './components/TransactionList';
import AddTransactionForm from './components/AddTransactionForm';
import UserProfile from './components/UserProfile';

export default function App() {
  const [selectedUserId, setSelectedUserId] = useState(1);

    const parentStyle = {
        maxWidth: '600px',
        margin: '0 auto',
        padding: '20px'
    }

  return (
    <div style={parentStyle}>
      <h1>💼 Corporate Ledger Management</h1>
      
      <UserProfile personId={selectedUserId} />
      <AddTransactionForm />
      <TransactionList />
    </div>
  );
}
