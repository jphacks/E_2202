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
  const [os, setOS] = React.useState('');
  const [language, setLanguage] = React.useState('');
  const [error, setError] = React.useState('');
  const [analizedError, setAnalizedError] = React.useState('');
  const [isShowAnalizedResults, setIsShowAnalizedResults] =
    React.useState(false);
  const [highlights, setHighlights] = React.useState([]);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [openSnackbar, setOpenSnackbar] = React.useState(false);
  const BACKEND_ENDPOINT = process.env.NEXT_PUBLIC_BACKEND_ENDPOINT;

  const router = useRouter();

  const handleChangeOS = (event: SelectChangeEvent) => {
    setOS(event.target.value as string);
  };

  const handleChangeLanguage = (event: SelectChangeEvent) => {
    setLanguage(event.target.value as string);
  };

  const handleChangeError = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError(event.target.value as string);
    setIsShowAnalizedResults(false);
    setAnalizedError('');
    setHighlights([]);
    setSearchQuery('');
  };

  const handleClickAnalyze = () => {
    if (error.length > 0) {
      fetch(`${BACKEND_ENDPOINT}/error_parse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: language, error_text: error }),
      })
        .then((res) => res.json())
        .then((data) => {
          setLanguage(data.parser);
          setIsShowAnalizedResults(true);
          setAnalizedError(error);
          setHighlights(data.result);
          const texts = data.result.map((x: { text: string; type: number }) =>
            x.type == 1 ? x.text : '',
          ) as [];
          const uniqueTexts = Array.from(new Set(texts).values());
          setSearchQuery(buildSearchQuery(uniqueTexts as []));
          return router.push('#result-content');
        })
        .catch((error) => {
          console.error('通信に失敗しました', error);
        });
    }
  };

  const handleClickSearch = () => {
    fetch(`${BACKEND_ENDPOINT}/error_parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ language: language, error_text: error }),
    })
      .then((res) => res.json())
      .then((data) => {
        const texts = data.result.map((x: { text: string; type: number }) =>
          x.type == 1 ? x.text : '',
        ) as [];
        const uniqueTexts = Array.from(new Set(texts).values());
        const searchQuery = buildSearchQuery(uniqueTexts as [])
          .split(' ')
          .join('+');
        open(`https://google.com/search?q=${searchQuery}&lr=lang_ja`);
      })
      .catch((error) => {
        console.error('通信に失敗しました', error);
      });
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
    // 検索候補が減ってしまうため、一旦クエリに含めないようにしておく
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
                エラー文
              </FormHelperText>
              <OutlinedInput
                placeholder='解決したいエラー文を入力してくだい。'
                id='errorText'
                value={error}
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
                言語
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
                <MenuItem value={''}>指定なし</MenuItem>
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
                <MenuItem value={''}>指定なし</MenuItem>
                <MenuItem value={'macOS'}>macOS</MenuItem>
                {/* <MenuItem value={'Windows'}>Windows</MenuItem> */}
              </Select>
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
              解析
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
                  解析結果
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
                  検索クエリ候補
                </Typography>
                <FormControl fullWidth>
                  <FormHelperText
                    component='div'
                    sx={{
                      m: 0,
                      fontSize: '1rem',
                    }}
                  >
                    検索文字列
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
                  検索
                </Button>
              </Stack>
            </Container>
          </Box>
        </>
      )}
    </Box>
  );
}
