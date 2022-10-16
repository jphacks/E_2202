import * as React from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';

export default function Search() {
  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          my: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Search
        </Typography>

        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          fullWidth
          // value={age}
          label="Age"
          // onChange={handleChange}
        >
          <MenuItem value={1}>Python</MenuItem>
          <MenuItem value={2}>JavaScript</MenuItem>
          <MenuItem value={3}>Ruby</MenuItem>
        </Select>

        <p>

        </p>

        <TextField
          id="outlined-multiline-static"
          label="Multiline"
          fullWidth
          multiline
          rows={10}
          defaultValue="Default Value"
        />
      </Box>
    </Container>
  );
}