// Header.js
import React, { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';

const Header = () => {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    return (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', padding: 2, backgroundColor: '#333', color: 'white' }}>
            <Typography variant="h6">Dashboard</Typography>
            <Typography variant="h6">{time.toLocaleTimeString()}</Typography>
        </Box>
    );
};

export default Header;
