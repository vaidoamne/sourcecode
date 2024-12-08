import React from 'react';
import { Box, Grid, Typography, Card, CardActionArea, CardContent, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import TrainIcon from '@mui/icons-material/Train';
import SupportIcon from '@mui/icons-material/Support';
import TrackChangesIcon from '@mui/icons-material/TrackChanges';
import AddBoxIcon from '@mui/icons-material/AddBox';
import Header from '../../Components/header/header';
import './home.css';

const Home = () => {
    const widgets = [
        { title: 'Book Ticket', icon: <TrainIcon fontSize="large" />, path: '/book-ticket' },
        { title: 'Track Train', icon: <TrackChangesIcon fontSize="large" />, path: '/track-train' },
        { title: 'Support', icon: <SupportIcon fontSize="large" />, path: '/support' },
        { title: 'Widget 4', icon: <AddBoxIcon fontSize="large" />, path: '/widget-4' },
        { title: 'Future Feature', icon: <AddBoxIcon fontSize="large" />, path: '#' },
        { title: 'Future Feature', icon: <AddBoxIcon fontSize="large" />, path: '#' },
    ];

    return (
        <div className="body">
            <Header />
            <Box sx={{ padding: 3 }}>
                <Box textAlign="center" mb={4}>
                    <Typography variant="h4" color="white">Welcome to the Awesome Dashboard</Typography>
                    <Link to="/">
                        <Button variant="contained" color="primary" sx={{ mt: 2 }}>
                            Back to Landing Page
                        </Button>
                    </Link>
                </Box>

                <Grid container spacing={2} justifyContent="center">
                    {widgets.map((widget, index) => (
                        <Grid item xs={12} sm={6} md={4} key={index}>
                            <Card className="widget">
                                <CardActionArea component={Link} to={widget.path}>
                                    <CardContent sx={{ textAlign: 'center' }} className='widget-inside'>
                                        {widget.icon}
                                        <Typography variant="h6" mt={2}>
                                            {widget.title}
                                        </Typography>
                                    </CardContent>
                                </CardActionArea>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </div>
    );
};

export default Home;
