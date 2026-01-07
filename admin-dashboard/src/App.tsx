// admin-dashboard/src/App.tsx or index.tsx
import React from 'react';
import { ApolloClient, InMemoryCache } from '@apollo/client';
import { ApolloProvider } from '@apollo/client/react';
import { HttpLink } from '@apollo/client/link/http';
import Dashboard from './pages/Dashboard';

// Create HTTP link - hardcoded for now
const httpLink = new HttpLink({
  uri: 'http://localhost:8000/graphql', // Django default
});

// Alternative: Use relative path if backend is on same origin
// const httpLink = new HttpLink({
//   uri: '/graphql',
// });

// Create Apollo Client
const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
});

function App() {
  return (
    <ApolloProvider client={client}>
      <Dashboard />
    </ApolloProvider>
  );
}

export default App;