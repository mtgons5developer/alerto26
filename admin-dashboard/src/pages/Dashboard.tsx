// admin-dashboard/src/pages/Dashboard.tsx
import React from 'react';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useQuery } from '@apollo/client/react';
import { gql } from '@apollo/client';

// Define TypeScript interfaces for your data
interface Emergency {
  id: string;
  code: string;
  emergencyType: string;
  priority: string;
  status: string;
  createdAt: string;
}

interface Provider {
  id: string;
  status: string;
  serviceTypes: string[];
}

interface DashboardStatsData {
  activeEmergencies: Emergency[];
  providers: Provider[];
}

const DASHBOARD_STATS = gql`
  query DashboardStats {
    activeEmergencies {
      id
      code
      emergencyType
      priority
      status
      createdAt
    }
    providers {
      id
      status
      serviceTypes
    }
  }
`;

const Dashboard: React.FC = () => {
  const { loading, error, data } = useQuery<DashboardStatsData>(DASHBOARD_STATS, {
    pollInterval: 10000,
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const activeCount = data?.activeEmergencies?.length || 0;
  const availableProviders = data?.providers?.filter(p => p.status === 'AVAILABLE').length || 0;

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        RescueLink Dashboard
      </Typography>
      
      {/* MUI v7 Grid syntax */}
      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 3 }}>  {/* Use 'size' prop */}
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">Active Emergencies</Typography>
            <Typography variant="h3" color="error">{activeCount}</Typography>
          </Paper>
        </Grid>
        
        <Grid size={{ xs: 12, md: 3 }}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">Available Providers</Typography>
            <Typography variant="h3" color="success.main">{availableProviders}</Typography>
          </Paper>
        </Grid>
      </Grid>
      
      {/* ... rest of component ... */}
    </Box>
  );
};

export default Dashboard;