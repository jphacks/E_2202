import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import {
  Alert,
  Box,
  Button,
  Container,
  Fade,
  FormControl,
  FormHelperText,
  MenuItem,
  IconButton,
  InputAdornment,
  OutlinedInput,
  Select,
  Stack,
  Typography,
  SelectChangeEvent,
} from '@mui/material';
import Head from 'next/head';
import { useRouter } from 'next/router';
import * as React from 'react';
import CodeArea from '../src/components/codeArea';
import Header from '../src/components/header';

export default function Search() {
  const [rawError, setRawError] = React.useState('');
  const [os, setOS] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [maskWords, setMaskWords] = React.useState('');
  const [analizedError, setAnalizedError] = React.useState('');
  const [isShowAnalizedResults, setIsShowAnalizedResults] =
    React.useState(false);
  const [highlights, setHighlights] = React.useState([]);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [openSnackbar, setOpenSnackbar] = React.useState(false);
  const BACKEND_ENDPOINT = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT;

  const router = useRouter();

  const handleChangeError = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRawError(event.target.value as string);
    setIsShowAnalizedResults(false);
    setAnalizedError('');
    setHighlights([]);
    setSearchQuery('');
  };

  const handleChangeOS = (event: SelectChangeEvent) => {
    setOS(event.target.value as string);
  };

  const handleChangeLanguage = (event: SelectChangeEvent) => {
    setLanguage(event.target.value as string);
  };

  const handleChangeMaskWords = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setMaskWords(event.target.value as string);
  };

  const handleClickAnalyze = () => {
    let errorText = rawError;
    if (errorText.length > 0) {
      if (maskWords.length > 0) {
        maskWords.split(',').forEach((word) => {
          errorText = errorText.replaceAll(word, 'xxx');
        });
      }

      fetch(`${BACKEND_ENDPOINT}/error_parse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: language, error_text: errorText }),
      })
        .then((res) => res.json())
        .then((data) => {
          setLanguage(data.parser);
          setIsShowAnalizedResults(true);
          setAnalizedError(errorText);
          setHighlights(data.result);
          const texts = data.result.map((x: { text: string; type: number }) =>
            x.type == 1 ? x.text : '',
          ) as [];
          const uniqueTexts = Array.from(new Set(texts).values());
          setSearchQuery(buildSearchQuery(uniqueTexts as []));
          return router.push('#result-content');
        })
        .catch((error) => {
          console.error('???????????????????????????', error);
        });
    }
  };

  const handleClickSearch = () => {
    const sq = searchQuery.split(' ').join('+');
    open(`https://google.com/search?q=${sq}&lr=lang_ja`);
  };

  const handleClickCopy = () => {
    navigator.clipboard.writeText(searchQuery);
    setOpenSnackbar(true);
  };

  const handleMouseDownCopy = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
  };

  const handleCloseCopyAlert = () => {
    setOpenSnackbar(false);
  };

  const buildSearchQuery = (queryErrorContents: []) => {
    let query = '';
    query += queryErrorContents.join(' ');
    // ?????????????????????????????????????????????????????????????????????????????????????????????
    // if (language !== '') {query += ` in ${language}`}
    // if (os !== '') {query += ` on ${os}`}
    return query;
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'grey.100' }}>
      <Head>
        <title>YouQuery</title>
      </Head>

      <Header />

      <Box sx={{ py: 4, bgcolor: 'grey.100' }}>
        <Container maxWidth='lg'>
          <Stack
            direction='column'
            justifyContent='center'
            alignItems='center'
            spacing={2}
          >
            <FormControl fullWidth>
              <FormHelperText
                component='div'
                sx={{
                  m: 0,
                  fontSize: '1rem',
                }}
              >
                ????????????
              </FormHelperText>
              <OutlinedInput
                placeholder='??????????????????????????????????????????????????????'
                id='errorText'
                value={rawError}
                onChange={handleChangeError}
                multiline
                rows={10}
                sx={{
                  bgcolor: 'white',
                }}
              />
            </FormControl>
            <FormControl fullWidth>
              <FormHelperText
                component='div'
                sx={{
                  m: 0,
                  fontSize: '1rem',
                }}
              >
                ??????
              </FormHelperText>
              <Select
                id='language'
                value={language}
                onChange={handleChangeLanguage}
                displayEmpty
                sx={{
                  bgcolor: 'white',
                }}
              >
                <MenuItem value={''}>????????????</MenuItem>
                <MenuItem value={'Python'}>Python</MenuItem>
                <MenuItem value={'Java'}>Java</MenuItem>
                <MenuItem value={'JavaScript'}>JavaScript</MenuItem>
                <MenuItem value={'Others'}>Others</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <FormHelperText
                component='div'
                sx={{
                  m: 0,
                  fontSize: '1rem',
                }}
              >
                OS
              </FormHelperText>
              <Select
                id='os'
                value={os}
                onChange={handleChangeOS}
                displayEmpty
                sx={{
                  bgcolor: 'white',
                }}
              >
                <MenuItem value={''}>????????????</MenuItem>
                <MenuItem value={'macOS'}>macOS</MenuItem>
                {/* <MenuItem value={'Windows'}>Windows</MenuItem> */}
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <FormHelperText
                component='div'
                sx={{
                  m: 0,
                  fontSize: '1rem',
                }}
              >
                ????????????????????????
              </FormHelperText>
              <OutlinedInput
                placeholder='ProjectName,ModuleName'
                id='maskWords'
                value={maskWords}
                onChange={handleChangeMaskWords}
                sx={{
                  bgcolor: 'white',
                }}
              />
              <FormHelperText
                component='div'
                sx={{
                  m: 0,
                  fontSize: '0.75rem',
                }}
              >
                ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????xxx????????????????????????
              </FormHelperText>
            </FormControl>
          </Stack>
          <Stack
            direction='row'
            justifyContent='center'
            alignItems='center'
            sx={{ py: 4 }}
          >
            <Button
              variant='contained'
              sx={{
                width: 200,
                height: 50,
              }}
              onClick={handleClickAnalyze}
            >
              ??????
            </Button>
          </Stack>
        </Container>
      </Box>

      {isShowAnalizedResults && (
        <>
          <Box sx={{ pt: 4, pb: 8, bgcolor: 'white' }}>
            <Container maxWidth='lg'>
              <Stack
                direction='column'
                justifyContent='center'
                alignItems='center'
                spacing={2}
              >
                <Typography
                  id='result-content'
                  variant='h6'
                  component='h2'
                  gutterBottom
                >
                  ????????????
                </Typography>
                <CodeArea errorText={analizedError} highlights={highlights} />
              </Stack>
            </Container>
          </Box>

          <Box sx={{ py: 4, bgcolor: 'grey.100' }}>
            <Container maxWidth='lg'>
              <Stack
                direction='column'
                justifyContent='center'
                alignItems='center'
                spacing={2}
              >
                <Typography
                  id='result-content'
                  variant='h6'
                  component='h2'
                  gutterBottom
                >
                  ?????????????????????
                </Typography>
                <FormControl fullWidth>
                  <FormHelperText
                    component='div'
                    sx={{
                      m: 0,
                      fontSize: '1rem',
                    }}
                  >
                    ???????????????
                  </FormHelperText>
                  <OutlinedInput
                    inputProps={{ readOnly: true }}
                    value={searchQuery}
                    sx={{
                      bgcolor: 'white',
                    }}
                    endAdornment={
                      <InputAdornment position='end'>
                        <Box sx={{ zIndex: 'modal', pr: 1 }}>
                          <Fade in={openSnackbar}>
                            <Alert icon={false} severity='success'>
                              Copied
                            </Alert>
                          </Fade>
                        </Box>
                        <IconButton
                          aria-label='Click to copy'
                          onClick={handleClickCopy}
                          onMouseDown={handleMouseDownCopy}
                          onMouseOut={handleCloseCopyAlert}
                          edge='end'
                        >
                          <ContentCopyIcon />
                        </IconButton>
                      </InputAdornment>
                    }
                  />
                </FormControl>
              </Stack>
              <Stack
                direction='row'
                justifyContent='center'
                alignItems='center'
                sx={{ py: 4 }}
              >
                <Button
                  variant='contained'
                  sx={{ width: 200, height: 50 }}
                  onClick={handleClickSearch}
                >
                  ??????
                </Button>
              </Stack>
            </Container>
          </Box>
        </>
      )}
    </Box>
  );
}
