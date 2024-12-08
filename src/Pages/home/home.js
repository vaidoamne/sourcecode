import React from 'react';
import { Box, Grid, Typography, Card, CardActionArea, CardContent, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import TrainIcon from '@mui/icons-material/Train';
import SupportIcon from '@mui/icons-material/Support';
import TrackChangesIcon from '@mui/icons-material/TrackChanges';
import AddBoxIcon from '@mui/icons-material/AddBox';
import Header from '../../Components/header/header';
import './home.css';

import Carousel from "react-material-ui-carousel";
const Home = () => {
    const images = [
    "path/to/carouselle1.jpg",
    "path/to/carouselle2.jpg",
    "path/to/carouselle3.jpg",
    "path/to/carouselle4.jpg",
    "path/to/carouselle5.jpg",
  ];
    const widgets = [
        { title: 'Book Ticket', icon: <TrainIcon fontSize="large" />, path: '/book-ticket' },
        { title: 'Track Train', icon: <TrackChangesIcon fontSize="large" />, path: '/track-train' },
        { title: 'Support', icon: <SupportIcon fontSize="large" />, path: '/support' },
        { title: 'Widget 4', icon: <AddBoxIcon fontSize="large" />, path: '/widget-4' },
        { title: 'Future Feature', icon: <AddBoxIcon fontSize="large" />, path: '#' },
        { title: 'Future Feature', icon: <AddBoxIcon fontSize="large" />, path: '#' },
    ];
    const widgetscarousel = [
        {
            title: 'National Delays',
            data: [
                { label: 'Delay Average', value: '50 years' },
                { label: 'Number of Delays', value: '102,552' },
                { label: 'Tickets Raised', value: '520' },
            ],
        },
        {
            title: 'Regional Stats',
            data: [
                { label: 'Trains On Time', value: '85%' },
                { label: 'Average Speed', value: '80 km/h' },
                { label: 'Maintenance Requests', value: '12,345' },
            ],
        },
        {
            title: 'Passenger Insights',
            data: [
                { label: 'Total Passengers', value: '2.5 million' },
                { label: 'Tickets Sold', value: '1.8 million' },
                { label: 'Complaints Resolved', value: '98%' },
            ],
        },
        {
            title: 'Operational Metrics',
            data: [
                { label: 'Trains in Operation', value: '1,200' },
                { label: 'Fuel Usage', value: '300,000 liters/day' },
                { label: 'Accidents Avoided', value: '99%' },
            ],
        },
        {
            title: 'Future Projections',
            data: [
                { label: 'New Lines', value: '50' },
                { label: 'Expansion Budget', value: '$5 billion' },
                { label: 'Projected Growth', value: '20% YoY' },
            ],
        },
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
            <Grid container spacing={2} justifyContent="center">
                    <Grid item xs={12}>
                        <Box className= "carousel-box"
                        >
                            <Carousel
                                autoPlay={true}
                                indicators={true}
                                animation="slide"
                                
                                navButtonsAlwaysVisible={true}
                                cycleNavigation={true}
                                className='carousel-style'
                            >
                                {widgetscarousel.map((widgetscarousel, index) => (
                                    <Card key={index} className='carousel-card' sx={{
                                        height: "250px",
                                        background:"rgba(240, 160, 20, 0.8);",
                                        display: "flex",
                                        flexDirection: "column",
                                        justifyContent: "center",
                                        alignItems: "center", 
                                        }}>
                                        <CardContent sx={{ textAlign: "center" }}>
                                            <Typography variant="h5" sx={{ mb: 2, fontWeight: 'bold' }}>
                                                {widgetscarousel.title}
                                            </Typography>
                                            {widgetscarousel.data.map((item, idx) => (
                                                <Typography key={idx} variant="body1" sx={{ mb: 1 }}>
                                                    {item.label}: {item.value}
                                                </Typography>
                                            ))}
                                        </CardContent>
                                    </Card>
                                ))}
                            </Carousel>
                        </Box>
                    </Grid>
                </Grid>
            
        </div>
    );
};

export default Home;
