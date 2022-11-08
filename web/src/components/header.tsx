import {
  AppBar,
  Container,
  Toolbar,
  Typography,
  Box,
  Link,
} from '@mui/material';

export default function Header() {
  return (
    <Box>
      <AppBar
        position='relative'
        sx={{
          bgcolor: 'white',
          color: 'black',
          boxShadow: 0,
          borderBottom: 1,
          borderColor: 'grey.400',
        }}
      >
        <Container maxWidth='lg'>
          <Toolbar disableGutters>
            <Typography
              variant='h6'
              noWrap
              component='a'
              href='/'
              sx={{
                mr: 2,
                flexGrow: 0,
                fontFamily: 'monospace',
                fontWeight: 700,
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              YouQuery
            </Typography>
            <Box
              sx={{
                flexGrow: 1,
                display: 'flex',
                justifyContent: 'flex-end',
              }}
            >
              {/* <Link
                href='/'
                component='a'
                underline='none'
                sx={{
                  display: 'block',
                  p: 1,
                  color: 'inherit',
                }}
              >
                About
              </Link> */}
              <Link
                href='https://github.com/jphacks/E_2202'
                component='a'
                underline='none'
                sx={{
                  display: 'block',
                  p: 1,
                  color: 'inherit',
                }}
              >
                GitHub
              </Link>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>
      {/* <Box sx={{ height: '64px' }}></Box> */}
    </Box>
  );
}
