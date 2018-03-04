#include <iostream>
#include <log4cplus/helpers/loglog.h>
#include <log4cplus/logger.h>
#ifdef WITH_ICONV
#include <log4cplus/tchar.h>
#endif

using namespace std;
using namespace log4cplus::helpers;

void printMsgs() 
{
    cout << "Entering printMsgs()..." << endl;

    LogLog::getLogLog()->debug(LOG4CPLUS_TEXT("This is a Debug statement..."));
    LogLog::getLogLog()->debug(
        log4cplus::tstring(LOG4CPLUS_TEXT("This is a Debug statement...")));

    LogLog::getLogLog()->warn(LOG4CPLUS_TEXT("This is a Warning..."));
    LogLog::getLogLog()->warn(
        log4cplus::tstring(LOG4CPLUS_TEXT("This is a Warning...")));

    LogLog::getLogLog()->error(LOG4CPLUS_TEXT("This is a Error..."));
    LogLog::getLogLog()->error(
        log4cplus::tstring(LOG4CPLUS_TEXT("This is a Error...")));

    cout << "Exiting printMsgs()..." << endl << endl;
}


int main()
{
    printMsgs();

    cout << "Turning on debug..." << endl;
    LogLog::getLogLog()->setInternalDebugging(true);
    printMsgs();

    cout << "Turning on quiet mode..." << endl;
    LogLog::getLogLog()->setQuietMode(true);
    printMsgs();

#ifdef WITH_ICONV
    std::wstring wstr = log4cplus::helpers::towstring("test");
    std::string str = log4cplus::helpers::tostring(L"test");
#endif

    return 0;
}
