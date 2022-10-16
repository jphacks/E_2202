import * as React from 'react';
import type { NextPage } from 'next';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => ({
    main: {
      marginTop: theme.spacing(4),
      marginBottom: theme.spacing(4),
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    },
  }));

const Search: NextPage = () => {
    const classes = useStyles();

    return (
        <Container maxWidth="lg">
            <div className={classes.main}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Search
                </Typography>
            </div>
        </Container>
    );
}

export default Search;