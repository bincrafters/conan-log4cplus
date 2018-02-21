#include <log4cplus/helpers/loglog.h>
#include <log4cplus/logger.h>

using namespace log4cplus::helpers;

int main()
{
	log4cplus::Initializer initializer;
    LogLog::getLogLog()->debug(LOG4CPLUS_TEXT("This is a Debug statement..."));
    LogLog::getLogLog()->debug(
        log4cplus::tstring(LOG4CPLUS_TEXT("This is a Debug statement...")));

    return 0;
}
