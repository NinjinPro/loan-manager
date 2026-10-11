import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';

const fetchPersonById = async (id) => {
  const { data } = await apiClient(`/people/${id}`);
  return data;
};

export default function UserProfile({ personId }) {
  const { data: person, isLoading } = useQuery({
    queryKey: ['people', personId],
    queryFn: () => fetchPersonById(personId),
    enabled: !!personId,
  });

  if (!personId) return <div>Select a user to view their summary.</div>;
  if (isLoading) return <div>Loading profile...</div>;

  const divStyle = {
      border: '1px solid #ccc',
      padding: '10px'
  }

  return (
    <div style={divStyle}>
      <h4>Account Owner: {person.name}</h4>
      <p>Email Registered: {person.email}</p>
    </div>
  );
}
